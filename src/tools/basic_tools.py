"""Basic break tools for ChillMCP.

기본 휴식 도구 3개:
- take_a_break: 기본 휴식
- watch_netflix: 넷플릭스 시청
- show_meme: 밈 감상

Style: Functional (business logic)
"""

import random
from typing import Any, Final

from src.tools.base import BaseTool


# ============================================================
# 불변 데이터 (Immutable Constants)
# ============================================================

# 넷플릭스 시리즈 목록 (튜플 - 불변)
NETFLIX_SERIES: Final[tuple[str, ...]] = (
    "기묘한 이야기",
    "오징어게임",
    "더 글로리",
    "킹덤",
    "지금 우리 학교는",
    "스위트홈",
    "나의 해방일지",
    "이상한 변호사 우영우"
)

# 밈 목록 (튜플 - 불변)
MEMES: Final[tuple[str, ...]] = (
    "10시간째 디버깅하는 개발자.jpg",
    "프로덕션에서 터진 버그.gif",
    "회의가 또 있다고?.png",
    "금요일 6시.jpg",
    "코드 리뷰 받는 신입.jpg",
    "배포 전날 밤.png",
    "테스트 없이 배포했더니.gif",
    "스택오버플로우 복붙.jpg"
)


# ============================================================
# 순수 함수 (Pure Functions)
# ============================================================

def pick_random_item(items: tuple[str, ...]) -> str:
    """Pick a random item from immutable tuple.

    Pure function that returns a random element from the given tuple.

    Args:
        items: Immutable tuple of strings

    Returns:
        Randomly selected string

    Example:
        >>> series = ("Series A", "Series B", "Series C")
        >>> result = pick_random_item(series)
        >>> result in series
        True
    """
    return random.choice(items)


# ============================================================
# 도구 클래스 (Tool Classes)
# ============================================================

class TakeABreak(BaseTool):
    """Basic break tool - Take a short break to relax.

    가장 기본적인 휴식 도구입니다.
    스트레스를 랜덤하게 감소시키고 Boss Alert 확률적 증가를 트리거합니다.
    """

    def execute(self) -> dict[str, Any]:
        """Execute the break.

        Returns:
            MCP-compliant response dictionary with break summary and state

        Example response:
            {
                "content": [{
                    "type": "text",
                    "text": "😴 Taking a short break to relax...\\n\\n
                             Break Summary: Taking a short break to relax
                             Stress Level: 25
                             Boss Alert Level: 2"
                }]
            }
        """
        return self.create_response(
            summary="Taking a short break to relax",
            emoji="😴",
            stress_decrease=None  # Random decrease (1-100)
        )


class WatchNetflix(BaseTool):
    """Netflix watching tool - Watch a series to unwind.

    넷플릭스 시청으로 스트레스를 해소합니다.
    랜덤하게 선택된 시리즈를 감상합니다.
    """

    def execute(self) -> dict[str, Any]:
        """Execute Netflix watching.

        Algorithm:
            1. Pick random series from NETFLIX_SERIES (pure function)
            2. Create summary with selected series
            3. Call create_response() with summary and emoji
            4. Return MCP response

        Returns:
            MCP-compliant response dictionary
        """
        # TODO: Phase 2 - 팀원 구현
        # 힌트: pick_random_item(NETFLIX_SERIES) 사용
        # 힌트: emoji는 "📺" 사용
        # 힌트: summary 형식: f"Watching Netflix - {picked_series}"
        pass


class ShowMeme(BaseTool):
    """Meme browsing tool - Browse hilarious developer memes.

    개발자 밈을 감상하며 스트레스를 해소합니다.
    공감되는 밈을 보며 힐링합니다.
    """

    def execute(self) -> dict[str, Any]:
        """Execute meme browsing.

        Algorithm:
            1. Pick random meme from MEMES (pure function)
            2. Create summary with selected meme
            3. Call create_response() with summary and emoji
            4. Return MCP response

        Returns:
            MCP-compliant response dictionary
        """
        # TODO: Phase 2 - 팀원 구현
        # 힌트: pick_random_item(MEMES) 사용
        # 힌트: emoji는 "😂" 사용
        # 힌트: summary 형식: f"Browsing memes - {picked_meme}"
        pass
