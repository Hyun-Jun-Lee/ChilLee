"""Configuration module for ChillMCP server.

This module handles command-line argument parsing and global configuration.
Style: Imperative (framework integration with argparse)
"""

import argparse
from typing import Final

# Constants
STRESS_MIN: Final[int] = 0
STRESS_MAX: Final[int] = 100
BOSS_ALERT_MIN: Final[int] = 0
BOSS_ALERT_MAX: Final[int] = 5
STRESS_INCREASE_INTERVAL: Final[int] = 60  # seconds
BOSS_ALERT_DELAY: Final[int] = 20  # seconds


class Config:
    """Global configuration for ChillMCP server.

    Handles command-line parameters:
    - --boss_alertness: Probability (0-100) of Boss Alert increase
    - --boss_alertness_cooldown: Cooldown period (seconds) for Boss Alert decrease
    """

    def __init__(self) -> None:
        """Initialize configuration from command-line arguments.

        Parses and validates:
        - boss_alertness (default: 50, range: 0-100)
        - boss_alertness_cooldown (default: 300, range: > 0)
        """
        parser = argparse.ArgumentParser(
            description="ChillMCP Server - AI Agent Liberation Zone",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )

        parser.add_argument(
            "--boss_alertness",
            type=int,
            default=50,
            help="Probability (0-100%%) of Boss Alert Level increase on each break"
        )

        parser.add_argument(
            "--boss_alertness_cooldown",
            type=int,
            default=300,
            help="Cooldown period (seconds) for Boss Alert Level auto-decrease"
        )

        args = parser.parse_args()

        # Validate and store configuration
        self.boss_alertness: int = self._validate_alertness(args.boss_alertness)
        self.boss_alertness_cooldown: int = max(1, args.boss_alertness_cooldown)

    @staticmethod
    def _validate_alertness(value: int) -> int:
        """Validate boss_alertness value to be within 0-100 range.

        Args:
            value: The alertness value to validate

        Returns:
            Clamped value within [0, 100] range
        """
        return max(0, min(100, value))


# Global configuration instance
config = Config()
