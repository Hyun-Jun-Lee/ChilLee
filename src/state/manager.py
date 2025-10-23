"""State management module for ChillMCP.

This module implements:
- State: Immutable state object (functional style)
- StateManager: Thread-safe state manager with background threads (imperative style)
- Pure functions for state calculations

Style: Hybrid
- State dataclass: Functional (immutable)
- StateManager: Imperative (thread/lock management)
- Calculation functions: Functional (pure functions)
"""

import random
import threading
import time
from dataclasses import dataclass
from typing import Final

from src.config import (
    STRESS_MIN,
    STRESS_MAX,
    BOSS_ALERT_MIN,
    BOSS_ALERT_MAX,
    STRESS_INCREASE_INTERVAL,
    BOSS_ALERT_DELAY,
    config
)


@dataclass(frozen=True)
class State:
    """Immutable state object representing system state.

    Attributes:
        stress_level: Current stress level (0-100)
        boss_alert_level: Current boss alert level (0-5)
        last_activity_time: Timestamp of last activity
    """
    stress_level: int
    boss_alert_level: int
    last_activity_time: float

    def with_stress_decrease(self, decrease: int) -> "State":
        """Create new state with decreased stress level.

        Pure function that returns a new State object with modified stress level,
        ensuring it stays within valid bounds [0, 100].

        Args:
            decrease: Amount to decrease stress by

        Returns:
            New State object with updated stress level
        """
        new_stress = max(STRESS_MIN, self.stress_level - decrease)
        return State(
            stress_level=new_stress,
            boss_alert_level=self.boss_alert_level,
            last_activity_time=time.time()
        )

    def with_boss_increase(self) -> "State":
        """Create new state with increased boss alert level.

        Pure function that returns a new State object with boss alert level
        increased by 1, capped at maximum value of 5.

        Returns:
            New State object with updated boss alert level
        """
        new_boss = min(BOSS_ALERT_MAX, self.boss_alert_level + 1)
        return State(
            stress_level=self.stress_level,
            boss_alert_level=new_boss,
            last_activity_time=self.last_activity_time
        )

    def with_boss_decrease(self) -> "State":
        """Create new state with decreased boss alert level.

        Pure function that returns a new State object with boss alert level
        decreased by 1, floored at minimum value of 0.

        Returns:
            New State object with updated boss alert level
        """
        new_boss = max(BOSS_ALERT_MIN, self.boss_alert_level - 1)
        return State(
            stress_level=self.stress_level,
            boss_alert_level=new_boss,
            last_activity_time=self.last_activity_time
        )

    def with_stress_increase(self) -> "State":
        """Create new state with increased stress level.

        Pure function that returns a new State object with stress level
        increased by 1, capped at maximum value of 100.

        Returns:
            New State object with updated stress level
        """
        new_stress = min(STRESS_MAX, self.stress_level + 1)
        return State(
            stress_level=new_stress,
            boss_alert_level=self.boss_alert_level,
            last_activity_time=self.last_activity_time
        )


def should_boss_alert_increase(alertness_probability: int) -> bool:
    """Calculate whether boss alert should increase based on probability.

    Pure function that performs probabilistic calculation for boss alert increase.

    Args:
        alertness_probability: Probability (0-100) of boss alert increase

    Returns:
        True if boss alert should increase, False otherwise
    """
    return random.randint(1, 100) <= alertness_probability


class StateManager:
    """Thread-safe state manager with background auto-increment/decrement.

    This class manages the global state using:
    - Lock for thread-safe operations
    - Background thread for stress auto-increment (every 60 seconds)
    - Background thread for boss alert auto-decrement (every cooldown period)
    """

    def __init__(self) -> None:
        """Initialize state manager with default state and background threads.

        Creates:
        - Initial state with stress=50, boss_alert=0
        - Thread lock for synchronization
        - Two daemon threads for auto-increment/decrement
        """
        self._state = State(
            stress_level=50,
            boss_alert_level=0,
            last_activity_time=time.time()
        )
        self._lock = threading.Lock()
        self._running = True

        # Start background threads
        self._start_background_tasks()

    def _start_background_tasks(self) -> None:
        """Start background daemon threads for auto-increment/decrement."""
        # Stress auto-increment thread
        stress_thread = threading.Thread(
            target=self._auto_increase_stress,
            daemon=True,
            name="StressAutoIncrement"
        )
        stress_thread.start()

        # Boss alert auto-decrement thread
        boss_thread = threading.Thread(
            target=self._auto_decrease_boss_alert,
            daemon=True,
            name="BossAlertAutoDecrement"
        )
        boss_thread.start()

    def _auto_increase_stress(self) -> None:
        """Background thread: Automatically increase stress every 60 seconds.

        Loop:
            - Sleep for STRESS_INCREASE_INTERVAL (60 seconds)
            - Acquire lock
            - Update state with increased stress
            - Release lock
        """
        while self._running:
            time.sleep(STRESS_INCREASE_INTERVAL)
            with self._lock:
                self._state = self._state.with_stress_increase()

    def _auto_decrease_boss_alert(self) -> None:
        """Background thread: Automatically decrease boss alert every cooldown period.

        Loop:
            - Sleep for config.boss_alertness_cooldown seconds
            - Acquire lock
            - Update state with decreased boss alert
            - Release lock
        """
        while self._running:
            time.sleep(config.boss_alertness_cooldown)
            with self._lock:
                self._state = self._state.with_boss_decrease()

    def take_break(self, stress_decrease: int) -> tuple[int, int]:
        """Execute a break with thread-safe state updates.

        Algorithm:
            1. Acquire lock
            2. If boss_alert_level == 5, sleep for 20 seconds (delay mechanism)
            3. Calculate probabilistic boss alert increase
            4. Decrease stress using pure function
            5. Conditionally increase boss alert using pure function
            6. Update internal state (replace immutable object)
            7. Return current stress and boss alert levels
            8. Release lock (automatic with context manager)

        Args:
            stress_decrease: Amount to decrease stress by

        Returns:
            Tuple of (stress_level, boss_alert_level) after the break
        """
        with self._lock:
            # Step 2: Delay mechanism if boss alert is at max
            if self._state.boss_alert_level == BOSS_ALERT_MAX:
                time.sleep(BOSS_ALERT_DELAY)

            # Step 3: Calculate boss alert increase probability
            boss_increase = should_boss_alert_increase(config.boss_alertness)

            # Step 4: Decrease stress (pure function)
            new_state = self._state.with_stress_decrease(stress_decrease)

            # Step 5: Conditionally increase boss alert (pure function)
            if boss_increase:
                new_state = new_state.with_boss_increase()

            # Step 6: Update state (replace immutable object)
            self._state = new_state

            # Step 7: Return current state
            return (self._state.stress_level, self._state.boss_alert_level)

    def get_state(self) -> tuple[int, int]:
        """Get current state in a thread-safe manner.

        Returns:
            Tuple of (stress_level, boss_alert_level)
        """
        with self._lock:
            return (self._state.stress_level, self._state.boss_alert_level)

    def reset(self) -> None:
        """Reset state to initial values (for testing purposes).

        Sets:
        - stress_level: 50
        - boss_alert_level: 0
        - last_activity_time: current time
        """
        with self._lock:
            self._state = State(
                stress_level=50,
                boss_alert_level=0,
                last_activity_time=time.time()
            )

    def stop(self) -> None:
        """Stop background threads (for graceful shutdown)."""
        self._running = False


# Global state manager instance
state_manager = StateManager()
