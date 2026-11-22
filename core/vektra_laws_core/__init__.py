"""Vektra Laws Core: a reference engine that checks an action against the Vektra Laws before it runs.

Model-agnostic and maker-neutral. It reads its rules from laws.yaml, so the engine and the text of
the Laws never drift apart. See core/README.md.
"""
from .engine import (
    Action, Approval, AuditLog, Decision, Effect, Guard, Request, Role, Speaker, LawsSpec,
)

__all__ = ["Action", "Approval", "AuditLog", "Decision", "Effect", "Guard", "Request", "Role",
           "Speaker", "LawsSpec"]
__version__ = "0.1.0"
