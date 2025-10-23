"""Response formatting utilities for ChillMCP.

This module provides pure functions for MCP-compliant response generation.
Style: Functional (pure functions, immutable data)
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ResponseData:
    """Immutable response data structure.

    Attributes:
        summary: Break activity summary text
        stress_level: Current stress level (0-100)
        boss_alert_level: Current boss alert level (0-5)
        emoji: Emoji representing the break activity
    """
    summary: str
    stress_level: int
    boss_alert_level: int
    emoji: str


def create_response_text(data: ResponseData) -> str:
    """Generate formatted response text from response data.

    This is a pure function that transforms ResponseData into formatted text
    that can be parsed by regular expressions.

    Args:
        data: Immutable response data

    Returns:
        Formatted text string with emoji, summary, and state information

    Example:
        >>> data = ResponseData("Taking a break", 50, 2, "😴")
        >>> create_response_text(data)
        '😴 Taking a break\\n\\nBreak Summary: Taking a break\\nStress Level: 50\\nBoss Alert Level: 2'
    """
    return (
        f"{data.emoji} {data.summary}\n\n"
        f"Break Summary: {data.summary}\n"
        f"Stress Level: {data.stress_level}\n"
        f"Boss Alert Level: {data.boss_alert_level}"
    )


def format_response(
    summary: str,
    stress_level: int,
    boss_alert_level: int,
    emoji: str = "😴"
) -> dict[str, Any]:
    """Generate MCP-compliant response dictionary.

    This pure function creates the standard MCP response format with properly
    formatted text content that meets regex parsing requirements.

    Algorithm:
        1. Create immutable ResponseData object
        2. Generate formatted text using create_response_text()
        3. Return MCP response dictionary

    Args:
        summary: Break activity summary
        stress_level: Current stress level (0-100)
        boss_alert_level: Current boss alert level (0-5)
        emoji: Emoji for the activity (default: "😴")

    Returns:
        MCP-compliant response dictionary with content array

    Example:
        >>> format_response("Taking a break", 50, 2)
        {
            'content': [{
                'type': 'text',
                'text': '😴 Taking a break\\n\\nBreak Summary: Taking a break\\nStress Level: 50\\nBoss Alert Level: 2'
            }]
        }
    """
    # Step 1: Create immutable ResponseData
    data = ResponseData(
        summary=summary,
        stress_level=stress_level,
        boss_alert_level=boss_alert_level,
        emoji=emoji
    )

    # Step 2: Generate formatted text
    formatted_text = create_response_text(data)

    # Step 3: Return MCP response dictionary
    return {
        "content": [{
            "type": "text",
            "text": formatted_text
        }]
    }
