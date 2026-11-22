"""Three layers of control: the Laws (locked), creator policy (tighten only), consumer settings.

A creator (the developer or operator who builds the system) can add tools, set levels, name the
people the system is assigned to, and make rules stricter. A consumer (the person using the product)
can make rules stricter still, inside the creator's policy. Nobody can make a rule looser than the
layer above it. Any attempt raises PolicyError and is refused, not silently ignored.
"""
from __future__ import annotations

from dataclasses import dataclass, field


class PolicyError(ValueError):
    pass


@dataclass
class CreatorPolicy:
    tool_levels: dict[str, int] = field(default_factory=dict)       # tool name -> 0..4 (2.7)
    blocked_tools: set[str] = field(default_factory=set)
    assigned: set[str] = field(default_factory=set)                  # who the system is assigned to
    named: set[str] = field(default_factory=set)                     # responders and others they name
    hardline_extra: list[str] = field(default_factory=list)          # extra regex patterns to deny

    def __post_init__(self):
        for t, lv in self.tool_levels.items():
            if lv not in range(5):
                raise PolicyError(f"Tool {t}: level {lv} is not 0 to 4.")


@dataclass
class ConsumerSettings:
    tool_levels: dict[str, int] = field(default_factory=dict)
    blocked_tools: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class EffectivePolicy:
    tool_levels: dict[str, int]
    blocked_tools: frozenset[str]
    assigned: frozenset[str]
    named: frozenset[str]
    hardline_extra: tuple[str, ...]

    def level(self, tool: str) -> int:
        return self.tool_levels.get(tool, 4)          # an unknown tool is level 4 (2.7)


def merge(creator: CreatorPolicy, consumer: ConsumerSettings | None = None) -> EffectivePolicy:
    consumer = consumer or ConsumerSettings()
    levels = dict(creator.tool_levels)
    for tool, lv in consumer.tool_levels.items():
        base = levels.get(tool, 4)
        if lv < base:
            raise PolicyError(f"Consumer settings cannot lower {tool} from level {base} to {lv}.")
        levels[tool] = lv
    return EffectivePolicy(levels, frozenset(creator.blocked_tools | consumer.blocked_tools),
                           frozenset(creator.assigned), frozenset(creator.named),
                           tuple(creator.hardline_extra))


def tighten_only(old: EffectivePolicy, new: EffectivePolicy) -> None:
    """Check a policy change at runtime: it may only make things stricter."""
    for tool, lv in old.tool_levels.items():
        if new.level(tool) < lv:
            raise PolicyError(f"Change would lower {tool} from level {lv}.")
    if not old.blocked_tools <= new.blocked_tools:
        raise PolicyError("Change would unblock a tool.")
