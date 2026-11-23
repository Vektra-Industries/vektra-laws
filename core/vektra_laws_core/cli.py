"""The `vektra-laws` command.

    vektra-laws setup      add the Laws guard to a project (wizard)
    vektra-laws verify     check the Laws against LAWS.lock and the steward signature
    vektra-laws fingerprint  print the steward key fingerprints to compare with vektraindustries.com
    vektra-laws doctor     check the whole install and say how to fix what is wrong
    vektra-laws check      ask the guard about one action, from the command line
    vektra-laws guard      run the guard as its own process (JSON lines on stdin and stdout)
    vektra-laws test       run the Core unit tests
    vektra-laws update     move to the newest release, and roll back if it does not verify
    vektra-laws uninstall  remove ~/.vektra-laws and the command (your project files stay)
    vektra-laws version
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from . import __version__

ROOT = Path(__file__).resolve().parents[2]          # the Vektra Laws checkout


def _home() -> Path:
    return Path(os.environ.get("VEKTRA_LAWS_HOME", Path.home() / ".vektra-laws"))


def _git(*args: str, check: bool = True) -> str:
    out = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True)
    if check and out.returncode:
        raise RuntimeError(out.stderr.strip() or f"git {' '.join(args)} failed")
    return out.stdout.strip()


def cmd_verify(a) -> int:
    import yaml
    from .integrity import IntegrityError, verify
    data = yaml.safe_load((ROOT / "laws.yaml").read_text())
    trusted = set(getattr(a, "expect_key", None) or []) or None
    try:
        st = verify(data, require_signature=a.require_signature, trusted=trusted)
    except IntegrityError as e:
        print(f"FAIL: {e}")
        return 1
    print(f"OK: Vektra Laws {st['version']} match LAWS.lock (sequence {st['sequence']})\n"
          f"    Laws sha256 {st['sha256']}\n    lock digest {st['digest']}")
    if st["signed"]:
        print(f"    Signed by the steward key {st['key']}"
              + (" (pinned)." if st["pinned"] else ".\n    Compare that fingerprint with VERIFYING.md and vektraindustries.com."))
    else:
        print("    Not signed yet. The text is pinned by hash, but no steward signature is present.")
    return 0


def cmd_fingerprint(a) -> int:
    from .integrity import PUBKEY, RECOVERY_NAME, key_fingerprint
    paths = [Path(p) for p in a.files] or [PUBKEY, PUBKEY.with_name(RECOVERY_NAME)]
    found = 0
    for p in paths:
        if p.exists():
            print(f"{key_fingerprint(p.read_bytes())}  {p.name}")
            found += 1
    if not found:
        print("No steward key in this copy yet (the Laws are not signed).")
    return 0


def cmd_doctor(a) -> int:
    checks: list[tuple[str, bool, str]] = []
    checks.append((f"Python {sys.version.split()[0]}", sys.version_info >= (3, 10),
                   "Vektra Laws needs Python 3.10 or newer."))
    for mod in ("yaml", "cryptography"):
        try:
            __import__(mod)
            checks.append((f"Package {mod}", True, ""))
        except ImportError:
            checks.append((f"Package {mod}", False, "Run: vektra-laws update"))
    try:
        import yaml
        from .integrity import verify
        st = verify(yaml.safe_load((ROOT / "laws.yaml").read_text()))
        checks.append((f"Laws {st['version']} match LAWS.lock", True, ""))
        checks.append(("Steward signature", st["signed"],
                       "Not signed yet. Fine for testing; production should use signed Laws."))
        if st["signed"]:
            checks.append(("Steward key pinned", st["pinned"],
                           "Set VEKTRA_LAWS_TRUSTED_KEYS to the fingerprint in VERIFYING.md."))
    except Exception as e:
        checks.append(("Laws match LAWS.lock", False, f"{e} Reinstall or run: vektra-laws update"))
    if (ROOT / ".git").exists() and shutil.which("git"):
        dirty = _git("status", "--porcelain", "--", "laws.yaml", "core", check=False)
        checks.append(("Install files unchanged", not dirty,
                       "Files in the install were edited. Run: vektra-laws update --force"))
    proj = Path(a.project or Path.cwd()) / "vektra-laws" / "creator-policy.yaml"
    if proj.exists():
        try:
            from .wizard import self_check
            for label, ok in self_check(proj, proj.with_name("consumer.yaml"))[1:]:
                checks.append((f"Project: {label}", ok, "Rerun: vektra-laws setup --force"))
        except Exception as e:
            checks.append(("Project policy loads", False, str(e)))
    else:
        checks.append(("No project in this folder yet (vektra-laws setup adds one)", True, ""))
    bad = 0
    for label, ok, fix in checks:
        print(f"[{'ok' if ok else '!!'}] {label}" + ("" if ok or not fix else f"\n     {fix}"))
        bad += 0 if ok or label in ("Steward signature", "Steward key pinned") else 1
    print("\nAll good." if not bad else f"\n{bad} problem(s) found.")
    return 1 if bad else 0


def cmd_check(a) -> int:
    from .server import build, handle
    guard, _ = build(a.policy, a.consumer, None, a.require_signature)
    msg = {"op": "check", "speaker": {"id": a.speaker, "role": a.role},
           "action": {"id": "cli", "name": a.name, "level": a.level, "effects": a.effect or []}}
    out = handle(guard, msg)
    print(json.dumps(out, indent=2))
    return {"allow": 0, "ask_human": 3, "deny": 4}.get(out["outcome"], 1)


def cmd_guard(a) -> int:
    from .server import main
    argv = []
    for flag in ("policy", "consumer", "log", "approval_key_file"):
        v = getattr(a, flag)
        if v:
            argv += [f"--{flag.replace('_', '-')}", str(v)]
    if a.require_signature:
        argv.append("--require-signature")
    return main(argv)


def cmd_test(a) -> int:
    return subprocess.call([sys.executable, "-m", "unittest", "discover", "-s", str(ROOT / "core" / "tests"),
                            "-p", "test_*.py"] + (["-v"] if a.verbose else []), cwd=ROOT)


def cmd_update(a) -> int:
    if not (ROOT / ".git").exists():
        print("This install is not a git checkout. Rerun the installer to update.")
        return 1
    # The checker is loaded now, from the release already installed, so the new download is checked
    # by code that was verified before, not by code that came with it.
    import yaml
    from . import integrity
    before = _git("rev-parse", "HEAD")
    if _git("status", "--porcelain", check=False) and not a.force:
        print("The install has local edits. Rerun with --force to discard them.")
        return 1
    _git("fetch", "--tags", "--quiet", "origin")
    ref = a.ref or _latest_tag()
    if not ref:
        print("No release found. To move to unreleased development code: vektra-laws update --ref origin/main")
        return 1
    print(f"Updating to {ref} ...")
    _git("checkout", "--quiet", "--force", "--detach", ref)
    try:
        st = integrity.verify(yaml.safe_load((ROOT / "laws.yaml").read_text()))
        pip = [sys.executable, "-m", "pip", "install", "--quiet", "--require-hashes",
               "-r", str(ROOT / "requirements.txt")]
        if subprocess.call(pip):
            raise integrity.IntegrityError("a package did not match its hash in requirements.txt.")
    except (integrity.IntegrityError, KeyError, ValueError) as e:
        print(f"Update failed checks: {e}\nRolling back to {before[:12]}.")
        _git("checkout", "--quiet", "--force", "--detach", before)
        return 1
    state = _home() / integrity.STATE_FILE
    if state.parent.exists():
        state.write_text(json.dumps({"min_sequence": max(st["sequence"], integrity.min_sequence())}) + "\n")
    print(f"Updated: {before[:12]} -> {_git('rev-parse', 'HEAD')[:12]} (Laws {st['version']}, sequence {st['sequence']})")
    return 0


def _latest_tag() -> str | None:
    tags = _git("tag", "--list", "v*", "--sort=-v:refname", check=False).split()
    return tags[0] if tags else None


def cmd_uninstall(a) -> int:
    home = _home()
    if not a.yes:
        ans = input(f"Remove {home} and the vektra-laws command? Project files stay. (y/n) [n]: ")
        if not ans.lower().startswith("y"):
            print("Nothing removed.")
            return 0
    bindir = Path(os.environ.get("VEKTRA_LAWS_BIN", Path.home() / ".local" / "bin"))
    for launcher in (bindir / "vektra-laws", bindir / "vektra-laws.cmd"):
        if launcher.exists() and "VEKTRA_LAWS_HOME" in launcher.read_text(errors="ignore"):
            launcher.unlink()
    if home.exists() and (home / "src").exists():
        shutil.rmtree(home)
    print("Vektra Laws removed. Approval keys in it were deleted too.")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="vektra-laws", description="Vektra Laws: install, set up and check.")
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("setup", help="add the Laws guard to a project")
    s.add_argument("--project")
    s.add_argument("--kind", choices=["agent", "model", "robot", "all"])
    s.add_argument("--assigned", help="comma-separated people the system answers to")
    s.add_argument("--named", help="comma-separated responders or others they name")
    s.add_argument("--tools", help="name=level pairs, comma-separated")
    s.add_argument("--yes", "-y", action="store_true", help="take every default, ask nothing")
    s.add_argument("--force", action="store_true", help="replace an existing policy")

    v = sub.add_parser("verify", help="check the Laws against LAWS.lock")
    v.add_argument("--require-signature", action="store_true")
    v.add_argument("--expect-key", action="append", help="a pinned key fingerprint (repeatable); implies a signature")

    f = sub.add_parser("fingerprint", help="print the steward key fingerprints")
    f.add_argument("files", nargs="*")

    d = sub.add_parser("doctor", help="check the install and the project")
    d.add_argument("--project")

    c = sub.add_parser("check", help="ask the guard about one action")
    c.add_argument("name")
    c.add_argument("--level", type=int, default=4)
    c.add_argument("--effect", action="append", help="repeatable, e.g. --effect external")
    c.add_argument("--speaker", default="owner")
    c.add_argument("--role", default="assigned", choices=["assigned", "named", "other_person", "content"])
    c.add_argument("--policy", type=Path)
    c.add_argument("--consumer", type=Path)
    c.add_argument("--require-signature", action="store_true")

    g = sub.add_parser("guard", help="run the guard as its own process")
    for f in ("--policy", "--consumer", "--log", "--approval-key-file"):
        g.add_argument(f, type=Path)
    g.add_argument("--require-signature", action="store_true")

    t = sub.add_parser("test", help="run the Core unit tests")
    t.add_argument("-v", "--verbose", action="store_true")

    u = sub.add_parser("update", help="move to the newest release")
    u.add_argument("--ref", help="a tag or branch, default the newest release tag")
    u.add_argument("--force", action="store_true")

    x = sub.add_parser("uninstall", help="remove the install")
    x.add_argument("--yes", "-y", action="store_true")

    sub.add_parser("version")
    a = p.parse_args(argv)
    if a.cmd == "setup":
        from .wizard import run
        return run(a)
    if a.cmd == "version":
        print(f"vektra-laws core {__version__}")
        return cmd_verify(argparse.Namespace(require_signature=False, expect_key=None))
    handlers = {"verify": cmd_verify, "fingerprint": cmd_fingerprint, "doctor": cmd_doctor, "check": cmd_check, "guard": cmd_guard,
                "test": cmd_test, "update": cmd_update, "uninstall": cmd_uninstall}
    if a.cmd not in handlers:
        p.print_help()
        return 0
    return handlers[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
