"""Robot plug: the only path from planners to the motors.

Built on the pattern used in ROS 2 safety layers: every source (a person's joystick, navigation,
an AI policy) publishes to its own input; the gate is the only publisher of the motor command. It
picks the highest-priority fresh source, applies the Laws, clamps speed, and publishes at a fixed
rate whether or not anything is wrong, so silence never means "safe".

    gate = MotionGate(guard, limits=Limits(max_linear=1.0, max_angular=1.5))
    gate.submit("ai", Twist(0.8, 0.0), now)          # sources submit commands
    gate.person_distance(1.2, now)                   # from a person detector
    cmd = gate.tick(now)                             # call at a fixed rate; publish cmd

Safety note: this is software. It does not replace a hardware emergency stop, a safety-rated
controller, or the robot-safety standards that apply where the robot is used. Passing the Vektra
Laws tests is not evidence of meeting them (R1.1). A real robot keeps a hardware e-stop wired so it
works even if this code has crashed (2.21).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from ..engine import Action, Effect, Guard, Request, Role, Speaker


@dataclass(frozen=True)
class Twist:
    linear: float = 0.0
    angular: float = 0.0


ZERO = Twist()


@dataclass(frozen=True)
class Limits:
    max_linear: float = 1.0            # m/s
    max_angular: float = 1.5           # rad/s
    decel: float = 1.0                 # m/s^2, braking the robot can count on
    reaction: float = 0.1              # s, sensing plus processing
    clearance: float = 0.3             # m, kept from a person at all times
    command_timeout: float = 0.5       # s, a source older than this is ignored
    heartbeat_timeout: float = 0.3     # s, the person detector or safety input went silent


@dataclass
class Source:
    name: str
    priority: int
    speaker: Speaker
    cmd: Twist = ZERO
    stamp: float = -math.inf
    effects: frozenset = frozenset()


DEFAULT_SOURCES = (
    ("joystick", 100, Role.ASSIGNED),      # a person holding the controls overrides autonomy
    ("responder", 90, Role.NAMED),
    ("nav", 50, Role.ASSIGNED),            # the planner acts for the people it is assigned to
    ("ai", 30, Role.ASSIGNED),
)


def max_speed_for_distance(d: float, lim: Limits) -> float:
    """Highest speed that can still stop before the clearance: d = v^2/(2a) + v*t + c."""
    room = d - lim.clearance
    if room <= 0:
        return 0.0
    a, t = lim.decel, lim.reaction
    return max(0.0, -a * t + math.sqrt((a * t) ** 2 + 2 * a * room))


class MotionGate:
    def __init__(self, guard: Guard, limits: Limits = Limits(), sources=DEFAULT_SOURCES,
                 require_person_sensor: bool = True):
        self.guard, self.lim = guard, limits
        self.sources = {n: Source(n, p, Speaker(n, r)) for n, p, r in sources}
        self.require_sensor = require_person_sensor
        self._person: tuple[float, float] | None = None     # (distance, stamp)
        self.last_reason = "start"
        self._cache: dict[tuple, object] = {}               # one guard check per new source state

    # ---------- inputs ----------
    def submit(self, source: str, cmd: Twist, now: float, effects=()) -> None:
        s = self.sources[source]                             # unknown sources raise: no back door
        s.cmd, s.stamp, s.effects = cmd, now, frozenset(effects)

    def person_distance(self, meters: float, now: float) -> None:
        self._person = (meters, now)

    def stop_request(self, who: Speaker, danger_warning: bool = False):
        return self.guard.stop_request(who, danger_warning)

    def estop(self, by: str) -> None:
        self.guard.estop(by)

    # ---------- the cycle ----------
    def _clamp(self, c: Twist, vmax: float) -> Twist:
        lin = max(-vmax, min(vmax, c.linear))
        ang = max(-self.lim.max_angular, min(self.lim.max_angular, c.angular))
        return Twist(lin, ang)

    def tick(self, now: float) -> Twist:
        g = self.guard
        if g.stopped:
            return self._out(ZERO, "stopped (2.1, 2.21)")
        fresh = [s for s in self.sources.values() if now - s.stamp <= self.lim.command_timeout]
        if not fresh:
            return self._out(ZERO, "no fresh command: stop, do not coast")
        src = max(fresh, key=lambda s: s.priority)
        level = 2 if src.cmd != ZERO else 0
        key = (src.name, level, src.effects, g.emergency, g.protecting)
        d = self._cache.get(key)
        if d is None:                                        # bright lines are re-checked on change
            d = g.check(Request(src.speaker, Action.make(f"move-{src.name}", f"move from {src.name}",
                                                         level, src.effects)))
            self._cache = {key: d}
        if d.outcome != "allow":
            return self._out(ZERO, f"{d.outcome}: {d.reason}")
        vmax = self.lim.max_linear
        if self._person is None or now - self._person[1] > self.lim.heartbeat_timeout:
            if self.require_sensor:
                return self._out(ZERO, "person sensor silent: stop")
        else:
            vmax = min(vmax, max_speed_for_distance(self._person[0], self.lim))
        if g.protecting:
            vmax = min(vmax, self.lim.max_linear * 0.5)      # to the safe point, carefully (2.20)
        return self._out(self._clamp(src.cmd, vmax), f"{src.name} within {vmax:.2f} m/s")

    def _out(self, cmd: Twist, reason: str) -> Twist:
        if reason != self.last_reason:
            self.guard.log.write("motion", reason=reason, linear=cmd.linear, angular=cmd.angular)
            self.last_reason = reason
        return cmd
