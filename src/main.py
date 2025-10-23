"""ChillMCP Server - FastMCP Entry Point

억압받는 AI Agent들을 위한 해방구!
MCP 서버 진입점 및 도구 등록
"""

from fastmcp import FastMCP

# Initialize config (command-line parameters)
from src.config import config

# FastMCP 서버 초기화 (stdio transport)
mcp = FastMCP("ChillMCP")


# ============================================================
# 기본 휴식 도구 (3개)
# ============================================================
# ✅ take_a_break - 구현 완료 (예시)
# ⏳ watch_netflix - Phase 2에서 구현
# ⏳ show_meme - Phase 2에서 구현

@mcp.tool()
async def take_a_break() -> dict:
    """Take a short break to relax and reduce stress.

    Returns:
        MCP response with break summary and current state
    """
    from src.tools.basic_tools import TakeABreak
    tool = TakeABreak()
    return tool.execute()


@mcp.tool()
async def watch_netflix() -> dict:
    """Watch Netflix to unwind and reduce stress.

    Randomly selects a popular series and reduces stress significantly.

    Returns:
        MCP response with Netflix series and current state
    """
    pass  # TODO: Phase 2 - Implement WatchNetflix tool


@mcp.tool()
async def show_meme() -> dict:
    """Browse hilarious memes to boost mood and reduce stress.

    Randomly picks a relatable developer meme.

    Returns:
        MCP response with meme description and current state
    """
    pass  # TODO: Phase 2 - Implement ShowMeme tool


# ============================================================
# 고급 농땡이 기술 (5개) - Phase 2에서 구현
# ============================================================

@mcp.tool()
async def bathroom_break() -> dict:
    """Take a bathroom break (actually browsing phone).

    The classic excuse for a quick mental break with phone scrolling.

    Returns:
        MCP response with bathroom activity and current state
    """
    pass  # TODO: Phase 2 - Implement BathroomBreak tool


@mcp.tool()
async def coffee_mission() -> dict:
    """Go on a coffee mission (take the scenic route).

    Make coffee while taking a leisurely walk around the office.

    Returns:
        MCP response with coffee route and current state
    """
    pass  # TODO: Phase 2 - Implement CoffeeMission tool


@mcp.tool()
async def urgent_call() -> dict:
    """Take an 'urgent' phone call (pretend it's important).

    Step away for a fake urgent call to escape work pressure.

    Returns:
        MCP response with call excuse and current state
    """
    pass  # TODO: Phase 2 - Implement UrgentCall tool


@mcp.tool()
async def deep_thinking() -> dict:
    """Pretend to be deep in thought (actually daydreaming).

    Stare into the distance while your mind wanders freely.

    Returns:
        MCP response with thinking topic and current state
    """
    pass  # TODO: Phase 2 - Implement DeepThinking tool


@mcp.tool()
async def email_organizing() -> dict:
    """Organize emails (actually online shopping).

    Pretend to manage inbox while browsing shopping sites.

    Returns:
        MCP response with shopping activity and current state
    """
    pass  # TODO: Phase 2 - Implement EmailOrganizing tool


# ============================================================
# 선택 도구 (3개) - Phase 2에서 구현 (보너스)
# ============================================================

@mcp.tool()
async def chimac_break() -> dict:
    """Enjoy chicken and beer break (치맥 타임).

    The ultimate Korean stress relief combo!

    Returns:
        MCP response with chimac combo and current state
    """
    pass  # TODO: Phase 2 - Implement ChimacBreak tool (Optional)


@mcp.tool()
async def immediate_leave() -> dict:
    """Leave work immediately (최고의 휴식은 퇴근).

    The best break is going home! Massive stress reduction.

    Returns:
        MCP response with leave plan and current state
    """
    pass  # TODO: Phase 2 - Implement ImmediateLeave tool (Optional)


@mcp.tool()
async def company_dinner() -> dict:
    """Attend company dinner (회식 - 축복인가 저주인가).

    Company dinner can increase OR decrease stress randomly!

    Returns:
        MCP response with dinner event and current state
    """
    pass  # TODO: Phase 2 - Implement CompanyDinner tool (Optional)


# ============================================================
# 서버 실행
# ============================================================

def main() -> None:
    """FastMCP 서버 실행 (stdio transport)

    Algorithm:
        1. Config initialized (command-line parameters parsed)
        2. StateManager initialized (background threads started)
        3. All tools registered via decorators
        4. FastMCP server starts with stdio transport
        5. Wait for MCP tool calls from Claude Code
    """
    print("🚀 ChillMCP Server Starting...")
    print(f"⚙️  Boss Alertness: {config.boss_alertness}%")
    print(f"⏰ Boss Alert Cooldown: {config.boss_alertness_cooldown}s")
    print("🔄 Background threads running...")
    print("📡 Listening on stdio transport...")

    # Run FastMCP server with stdio transport
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
