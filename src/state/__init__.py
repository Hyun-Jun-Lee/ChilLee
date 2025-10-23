"""State management module for ChillMCP.

This module handles:
- Immutable State objects (functional)
- StateManager with thread-safe operations (imperative)
- Background threads for auto-increment/decrement
"""

from .manager import State, StateManager, state_manager

__all__ = ["State", "StateManager", "state_manager"]
