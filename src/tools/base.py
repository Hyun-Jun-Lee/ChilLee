"""Base tool module for ChillMCP break operations.

This module provides:
- ToolConfig: Immutable tool configuration (functional)
- Pure functions for tool logic (functional)
- BaseTool: Base class for all tools (imperative wrapper around functional core)

Style: Functional (business logic with pure functions)
"""

import random
from dataclasses import dataclass
from typing import Any, Optional

from src.state.manager import state_manager
from src.utils.response import format_response


@dataclass(frozen=True)
class ToolConfig:
    """Immutable tool configuration.

    Attributes:
        summary: Description of the break activity
        emoji: Emoji representing the activity
        stress_decrease: Amount to decrease stress (None for random)
    """
    summary: str
    emoji: str
    stress_decrease: Optional[int]


def calculate_stress_decrease_if_needed(stress_decrease: Optional[int]) -> int:
    """Calculate stress decrease amount, generating random value if needed.

    Pure function that returns either the provided value or generates a
    random value between 1 and 100.

    Args:
        stress_decrease: Optional stress decrease amount

    Returns:
        Final stress decrease amount (1-100)

    Example:
        >>> calculate_stress_decrease_if_needed(50)
        50
        >>> result = calculate_stress_decrease_if_needed(None)
        >>> 1 <= result <= 100
        True
    """
    if stress_decrease is None:
        return random.randint(1, 100)
    return stress_decrease


def create_tool_response(
    tool_config: ToolConfig,
    stress_level: int,
    boss_alert_level: int
) -> dict[str, Any]:
    """Generate tool response from configuration and current state.

    Pure function that creates MCP-compliant response by calling format_response.

    Args:
        tool_config: Immutable tool configuration
        stress_level: Current stress level after break
        boss_alert_level: Current boss alert level after break

    Returns:
        MCP-compliant response dictionary
    """
    return format_response(
        summary=tool_config.summary,
        stress_level=stress_level,
        boss_alert_level=boss_alert_level,
        emoji=tool_config.emoji
    )


class BaseTool:
    """Base class for all ChillMCP tools.

    Provides common functionality for executing breaks:
    - Stress decrease calculation (functional)
    - State management integration (imperative)
    - Response generation (functional)

    Subclasses should implement execute() method.
    """

    def create_response(
        self,
        summary: str,
        emoji: str = "😴",
        stress_decrease: Optional[int] = None
    ) -> dict[str, Any]:
        """Create tool response with state updates.

        Algorithm:
            1. Calculate stress_decrease using pure function
            2. Update state via state_manager (imperative)
            3. Create ToolConfig (immutable)
            4. Generate response using pure function
            5. Return response

        Args:
            summary: Break activity description
            emoji: Activity emoji (default: "😴")
            stress_decrease: Optional stress decrease amount (None for random)

        Returns:
            MCP-compliant response dictionary

        Example:
            >>> tool = BaseTool()
            >>> response = tool.create_response("Taking a break", "😴", 30)
            >>> response['content'][0]['type']
            'text'
        """
        # Step 1: Calculate stress decrease (functional)
        final_decrease = calculate_stress_decrease_if_needed(stress_decrease)

        # Step 2: Update state (imperative - side effect)
        stress_level, boss_alert_level = state_manager.take_break(final_decrease)

        # Step 3: Create immutable config
        tool_config = ToolConfig(
            summary=summary,
            emoji=emoji,
            stress_decrease=final_decrease
        )

        # Step 4: Generate response (functional)
        response = create_tool_response(
            tool_config=tool_config,
            stress_level=stress_level,
            boss_alert_level=boss_alert_level
        )

        # Step 5: Return response
        return response

    def execute(self) -> dict[str, Any]:
        """Execute the tool (to be implemented by subclasses).

        Subclasses should override this method to provide specific
        break implementations.

        Returns:
            MCP-compliant response dictionary

        Raises:
            NotImplementedError: If not overridden by subclass
        """
        raise NotImplementedError("Subclasses must implement execute()")
