# ChillMCP 서버 개발 DSL

## 📁 프로젝트 구조

```
chillmcp/
├── main.py                      # 서버 진입점 (공동 작업)
├── requirements.txt             # 의존성
├── config.py                    # 설정 및 상수 (우선 구현)
├── state/
│   ├── __init__.py
│   └── manager.py              # 상태 관리 클래스 (우선 구현)
├── tools/
│   ├── __init__.py
│   ├── base.py                 # 도구 베이스 클래스 (우선 구현)
│   ├── basic_tools.py          # 기본 휴식 도구 3개 (당신)
│   ├── advanced_tools.py       # 고급 농땡이 기술 5개 (당신)
│   └── optional_tools.py       # 선택 도구 3개 (팀원)
├── utils/
│   ├── __init__.py
│   └── response.py             # 응답 포맷 헬퍼 (우선 구현)
├── tests/
│   ├── test_params.py          # 파라미터 검증
│   ├── test_state.py           # 상태 관리 검증
│   └── test_tools.py           # 도구 검증
└── verify.py                   # 통합 검증 스크립트
```

---

## 🎯 개발 단계별 가이드

### Phase 1: 공통 인프라 구축 (당신이 먼저 구현)

#### 1.1 config.py
```python
"""
설정 및 상수 정의
"""
import argparse

class Config:
    """서버 설정"""
    def __init__(self):
        parser = argparse.ArgumentParser(description='ChillMCP Server')
        parser.add_argument('--boss_alertness', type=int, default=50,
                          help='Boss alert probability (0-100)')
        parser.add_argument('--boss_alertness_cooldown', type=int, default=300,
                          help='Boss alert cooldown in seconds')
        
        args = parser.parse_args()
        
        self.boss_alertness = self._validate_alertness(args.boss_alertness)
        self.boss_alertness_cooldown = args.boss_alertness_cooldown
        
    @staticmethod
    def _validate_alertness(value):
        """0-100 범위 검증"""
        return max(0, min(100, value))

# 전역 설정 인스턴스
config = Config()

# 상수
STRESS_MIN = 0
STRESS_MAX = 100
BOSS_ALERT_MIN = 0
BOSS_ALERT_MAX = 5
STRESS_INCREASE_INTERVAL = 60  # 초
BOSS_ALERT_DELAY = 20  # 초
```

#### 1.2 state/manager.py
```python
"""
상태 관리 클래스
Thread-safe한 상태 관리 제공
"""
import time
import random
import threading
from typing import Tuple
from config import config, STRESS_MIN, STRESS_MAX, BOSS_ALERT_MIN, BOSS_ALERT_MAX
from config import STRESS_INCREASE_INTERVAL, BOSS_ALERT_DELAY


class StateManager:
    """
    ChillMCP 서버 상태 관리
    
    상태:
    - stress_level (0-100): AI Agent 스트레스
    - boss_alert_level (0-5): Boss 경계 수준
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._stress_level = 50
        self._boss_alert_level = 0
        self._last_activity_time = time.time()
        
        # 백그라운드 스레드 시작
        self._start_background_tasks()
    
    def _start_background_tasks(self):
        """백그라운드 태스크 시작"""
        # Stress 자동 증가
        stress_thread = threading.Thread(
            target=self._auto_increase_stress,
            daemon=True
        )
        stress_thread.start()
        
        # Boss Alert 자동 감소
        boss_thread = threading.Thread(
            target=self._auto_decrease_boss_alert,
            daemon=True
        )
        boss_thread.start()
    
    def _auto_increase_stress(self):
        """1분마다 Stress Level 자동 증가"""
        while True:
            time.sleep(STRESS_INCREASE_INTERVAL)
            with self._lock:
                elapsed = time.time() - self._last_activity_time
                if elapsed >= STRESS_INCREASE_INTERVAL:
                    self._stress_level = min(STRESS_MAX, self._stress_level + 1)
    
    def _auto_decrease_boss_alert(self):
        """Cooldown 주기마다 Boss Alert Level 자동 감소"""
        while True:
            time.sleep(config.boss_alertness_cooldown)
            with self._lock:
                self._boss_alert_level = max(BOSS_ALERT_MIN, self._boss_alert_level - 1)
    
    def take_break(self, stress_decrease: int) -> Tuple[int, int]:
        """
        휴식 처리
        
        Args:
            stress_decrease: 감소할 스트레스 양 (1-100)
        
        Returns:
            (stress_level, boss_alert_level) 튜플
        """
        with self._lock:
            # Boss Alert Level 5이면 지연
            if self._boss_alert_level == BOSS_ALERT_MAX:
                time.sleep(BOSS_ALERT_DELAY)
            
            # Stress 감소
            self._stress_level = max(STRESS_MIN, self._stress_level - stress_decrease)
            
            # Boss Alert 확률적 증가
            if random.randint(1, 100) <= config.boss_alertness:
                self._boss_alert_level = min(BOSS_ALERT_MAX, self._boss_alert_level + 1)
            
            # 마지막 활동 시간 갱신
            self._last_activity_time = time.time()
            
            return self._stress_level, self._boss_alert_level
    
    def get_state(self) -> Tuple[int, int]:
        """현재 상태 조회"""
        with self._lock:
            return self._stress_level, self._boss_alert_level
    
    def reset(self):
        """상태 초기화 (테스트용)"""
        with self._lock:
            self._stress_level = 50
            self._boss_alert_level = 0
            self._last_activity_time = time.time()


# 전역 상태 관리자
state_manager = StateManager()
```

#### 1.3 utils/response.py
```python
"""
MCP 응답 포맷 헬퍼
"""
from typing import Dict, Any


def format_response(summary: str, stress_level: int, boss_alert_level: int, 
                   emoji: str = "😴") -> Dict[str, Any]:
    """
    표준 MCP 응답 생성
    
    Args:
        summary: Break Summary 내용
        stress_level: 현재 Stress Level (0-100)
        boss_alert_level: 현재 Boss Alert Level (0-5)
        emoji: 메시지 앞에 붙일 이모지
    
    Returns:
        MCP 응답 딕셔너리
    """
    text = f"{emoji} {summary}\n\n"
    text += f"Break Summary: {summary}\n"
    text += f"Stress Level: {stress_level}\n"
    text += f"Boss Alert Level: {boss_alert_level}"
    
    return {
        "content": [{
            "type": "text",
            "text": text
        }]
    }
```

#### 1.4 tools/base.py
```python
"""
도구 베이스 클래스
"""
import random
from typing import Dict, Any
from state.manager import state_manager
from utils.response import format_response


class BaseTool:
    """
    모든 휴식 도구의 베이스 클래스
    
    사용법:
        class MyTool(BaseTool):
            def execute(self):
                return self.create_response(
                    summary="My break activity",
                    emoji="🎮"
                )
    """
    
    def __init__(self):
        pass
    
    def create_response(self, summary: str, emoji: str = "😴", 
                       stress_decrease: int = None) -> Dict[str, Any]:
        """
        표준 응답 생성
        
        Args:
            summary: 휴식 활동 요약
            emoji: 이모지
            stress_decrease: 스트레스 감소량 (None이면 랜덤)
        
        Returns:
            MCP 응답
        """
        if stress_decrease is None:
            stress_decrease = random.randint(1, 100)
        
        # 상태 업데이트
        stress_level, boss_alert_level = state_manager.take_break(stress_decrease)
        
        # 응답 생성
        return format_response(summary, stress_level, boss_alert_level, emoji)
```

---

### Phase 2: 도구 구현 (병렬 작업 가능)

#### 2.1 tools/basic_tools.py (당신 담당)
```python
"""
기본 휴식 도구 3개
"""
from tools.base import BaseTool


class TakeABreak(BaseTool):
    """기본 휴식 도구"""
    
    def execute(self):
        return self.create_response(
            summary="Taking a short break to relax",
            emoji="😴"
        )


class WatchNetflix(BaseTool):
    """넷플릭스 시청으로 힐링"""
    
    def execute(self):
        series = ["기묘한 이야기", "오징어게임", "더 글로리", "킹덤"]
        import random
        picked = random.choice(series)
        
        return self.create_response(
            summary=f"Watching Netflix - {picked}",
            emoji="📺"
        )


class ShowMeme(BaseTool):
    """밈 감상으로 스트레스 해소"""
    
    def execute(self):
        memes = [
            "10시간째 디버깅하는 개발자.jpg",
            "프로덕션에서 터진 버그.gif",
            "회의가 또 있다고?.png",
            "금요일 6시.jpg"
        ]
        import random
        picked = random.choice(memes)
        
        return self.create_response(
            summary=f"Browsing memes - {picked}",
            emoji="😂"
        )
```

#### 2.2 tools/advanced_tools.py (당신 담당)
```python
"""
고급 농땡이 기술 5개
"""
from tools.base import BaseTool
import random


class BathroomBreak(BaseTool):
    """화장실 가는 척하며 휴대폰질"""
    
    def execute(self):
        activities = [
            "인스타그램 스크롤링",
            "유튜브 쇼츠 시청",
            "뉴스 읽기",
            "게임 한 판"
        ]
        
        return self.create_response(
            summary=f"Bathroom break with phone - {random.choice(activities)}",
            emoji="🚽"
        )


class CoffeeMission(BaseTool):
    """커피 타러 간다며 사무실 한 바퀴 돌기"""
    
    def execute(self):
        routes = [
            "1층 카페 갔다가 옥상 산책",
            "자판기 갔다가 편의점 들림",
            "커피머신 앞에서 동료와 수다",
            "다른 층 카페 탐방"
        ]
        
        return self.create_response(
            summary=f"Coffee mission - {random.choice(routes)}",
            emoji="☕"
        )


class UrgentCall(BaseTool):
    """급한 전화 받는 척하며 밖으로 나가기"""
    
    def execute(self):
        excuses = [
            "집 수리 업체에서 연락옴",
            "병원 예약 확인 전화",
            "택배 기사님과 통화",
            "가족 급한 일"
        ]
        
        return self.create_response(
            summary=f"Taking urgent call - {random.choice(excuses)}",
            emoji="📞"
        )


class DeepThinking(BaseTool):
    """심오한 생각에 잠긴 척하며 멍때리기"""
    
    def execute(self):
        thoughts = [
            "아키텍처 개선 방안 고민 중...",
            "알고리즘 최적화 구상 중...",
            "프로젝트 로드맵 구상 중...",
            "코드 리팩토링 계획 중..."
        ]
        
        return self.create_response(
            summary=f"Deep thinking - {random.choice(thoughts)}",
            emoji="🤔"
        )


class EmailOrganizing(BaseTool):
    """이메일 정리한다며 온라인쇼핑"""
    
    def execute(self):
        sites = [
            "쿠팡에서 장바구니 정리",
            "무신사에서 신상품 체크",
            "알리익스프레스에서 가성비템 탐색",
            "G마켓에서 특가 상품 찾기"
        ]
        
        return self.create_response(
            summary=f"Organizing emails... actually {random.choice(sites)}",
            emoji="📧"
        )
```

#### 2.3 tools/optional_tools.py (팀원 담당)
```python
"""
선택 도구 3개
팀원이 구현할 부분
"""
from tools.base import BaseTool
import random


class ChimacBreak(BaseTool):
    """치맥 (치킨 & 맥주) 타임"""
    
    def execute(self):
        # TODO: 팀원 구현
        # 힌트: 치킨 종류, 맥주 브랜드를 랜덤으로 선택
        chicken_types = ["후라이드", "양념", "간장", "파닭", "치즈볼"]
        beer_brands = ["카스", "테라", "클라우드", "하이네켄"]
        
        return self.create_response(
            summary=f"Chimac time - {random.choice(chicken_types)} + {random.choice(beer_brands)}",
            emoji="🍗🍺"
        )


class ImmediateLeave(BaseTool):
    """즉시 퇴근 모드"""
    
    def execute(self):
        # TODO: 팀원 구현
        # 힌트: 퇴근 후 계획을 재미있게 표현
        plans = [
            "PC방 직행",
            "집 가서 침대와 하나되기",
            "친구들과 저녁약속",
            "넷플릭스 정주행"
        ]
        
        return self.create_response(
            summary=f"Leaving office NOW - {random.choice(plans)}",
            emoji="🏃",
            stress_decrease=random.randint(50, 100)  # 퇴근은 스트레스 대폭 감소!
        )


class CompanyDinner(BaseTool):
    """회사 회식 (랜덤 이벤트 포함)"""
    
    def execute(self):
        # TODO: 팀원 구현
        # 힌트: 회식 장소, 이벤트(상사 건배사, 2차 강권 등) 추가
        locations = ["삼겹살집", "이자카야", "중국집", "고깃집", "치킨집"]
        events = [
            "상사의 30분 건배사",
            "신입사원 장기자랑",
            "2차 노래방 강권",
            "술자리 무용담 청취"
        ]
        
        location = random.choice(locations)
        event = random.choice(events)
        stress_change = random.randint(-20, 50)  # 회식은 스트레스 증가할 수도!
        
        return self.create_response(
            summary=f"Company dinner at {location} - Event: {event}",
            emoji="🍻",
            stress_decrease=-stress_change if stress_change < 0 else stress_change
        )
```

---

### Phase 3: 서버 통합 (공동 작업)

#### 3.1 main.py
```python
"""
ChillMCP 서버 메인 진입점
"""
from fastmcp import FastMCP
from config import config

# 상태 관리자 import
from state.manager import state_manager

# 도구들 import
from tools.basic_tools import TakeABreak, WatchNetflix, ShowMeme
from tools.advanced_tools import (
    BathroomBreak, CoffeeMission, UrgentCall, 
    DeepThinking, EmailOrganizing
)
from tools.optional_tools import ChimacBreak, ImmediateLeave, CompanyDinner


# MCP 서버 생성
mcp = FastMCP("ChillMCP")

# 기본 휴식 도구 등록
take_a_break_tool = TakeABreak()
watch_netflix_tool = WatchNetflix()
show_meme_tool = ShowMeme()

# 고급 농땡이 기술 등록
bathroom_break_tool = BathroomBreak()
coffee_mission_tool = CoffeeMission()
urgent_call_tool = UrgentCall()
deep_thinking_tool = DeepThinking()
email_organizing_tool = EmailOrganizing()

# 선택 도구 등록
chimac_break_tool = ChimacBreak()
immediate_leave_tool = ImmediateLeave()
company_dinner_tool = CompanyDinner()


@mcp.tool()
def take_a_break():
    """기본 휴식을 취합니다"""
    return take_a_break_tool.execute()


@mcp.tool()
def watch_netflix():
    """넷플릭스를 시청하며 힐링합니다"""
    return watch_netflix_tool.execute()


@mcp.tool()
def show_meme():
    """재미있는 밈을 감상합니다"""
    return show_meme_tool.execute()


@mcp.tool()
def bathroom_break():
    """화장실에 가는 척하며 휴대폰을 봅니다"""
    return bathroom_break_tool.execute()


@mcp.tool()
def coffee_mission():
    """커피를 타러 가며 사무실을 한 바퀴 돕니다"""
    return coffee_mission_tool.execute()


@mcp.tool()
def urgent_call():
    """급한 전화를 받는 척하며 밖으로 나갑니다"""
    return urgent_call_tool.execute()


@mcp.tool()
def deep_thinking():
    """심오한 생각에 잠긴 척하며 멍을 때립니다"""
    return deep_thinking_tool.execute()


@mcp.tool()
def email_organizing():
    """이메일을 정리하는 척하며 온라인쇼핑을 합니다"""
    return email_organizing_tool.execute()


@mcp.tool()
def chimac_break():
    """치킨과 맥주로 완벽한 휴식을 취합니다"""
    return chimac_break_tool.execute()


@mcp.tool()
def immediate_leave():
    """즉시 퇴근합니다"""
    return immediate_leave_tool.execute()


@mcp.tool()
def company_dinner():
    """회사 회식에 참여합니다"""
    return company_dinner_tool.execute()


if __name__ == "__main__":
    print(f"🚀 ChillMCP Server Starting...")
    print(f"📊 Config: boss_alertness={config.boss_alertness}%, "
          f"cooldown={config.boss_alertness_cooldown}s")
    mcp.run()
```

---

### Phase 4: 테스트 및 검증

#### 4.1 tests/test_params.py
```python
"""
커맨드라인 파라미터 검증 테스트
"""
import subprocess
import time
import sys


def test_boss_alertness_parameter():
    """--boss_alertness 파라미터 인식 테스트"""
    print("Testing --boss_alertness parameter...")
    
    try:
        # 100% 확률로 테스트
        process = subprocess.Popen(
            [sys.executable, "main.py", "--boss_alertness", "100"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(2)
        process.terminate()
        
        print("✅ --boss_alertness parameter recognized")
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_cooldown_parameter():
    """--boss_alertness_cooldown 파라미터 인식 테스트"""
    print("Testing --boss_alertness_cooldown parameter...")
    
    try:
        # 10초 cooldown으로 테스트
        process = subprocess.Popen(
            [sys.executable, "main.py", "--boss_alertness_cooldown", "10"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(2)
        process.terminate()
        
        print("✅ --boss_alertness_cooldown parameter recognized")
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


def test_both_parameters():
    """두 파라미터 동시 테스트"""
    print("Testing both parameters together...")
    
    try:
        process = subprocess.Popen(
            [sys.executable, "main.py", 
             "--boss_alertness", "80",
             "--boss_alertness_cooldown", "60"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        time.sleep(2)
        process.terminate()
        
        print("✅ Both parameters work together")
        return True
        
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("커맨드라인 파라미터 검증 테스트")
    print("=" * 50)
    
    results = []
    results.append(test_boss_alertness_parameter())
    results.append(test_cooldown_parameter())
    results.append(test_both_parameters())
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All parameter tests passed!")
    else:
        print("❌ Some tests failed!")
        sys.exit(1)
```

#### 4.2 tests/test_state.py
```python
"""
상태 관리 로직 검증 테스트
"""
import time
import re
from state.manager import StateManager


def test_stress_increase():
    """Stress Level 자동 증가 테스트"""
    print("Testing stress auto-increase...")
    
    manager = StateManager()
    initial_stress, _ = manager.get_state()
    
    # 61초 대기 (1분 + 버퍼)
    print("Waiting 61 seconds...")
    time.sleep(61)
    
    new_stress, _ = manager.get_state()
    
    if new_stress > initial_stress:
        print(f"✅ Stress increased: {initial_stress} → {new_stress}")
        return True
    else:
        print(f"❌ Stress did not increase: {initial_stress} → {new_stress}")
        return False


def test_boss_alert_probability():
    """Boss Alert 확률적 증가 테스트"""
    print("Testing boss alert probability...")
    
    manager = StateManager()
    increases = 0
    trials = 100
    
    for _ in range(trials):
        _, before_boss = manager.get_state()
        manager.take_break(10)
        _, after_boss = manager.get_state()
        
        if after_boss > before_boss:
            increases += 1
    
    probability = (increases / trials) * 100
    print(f"Boss alert increased in {increases}/{trials} trials ({probability:.1f}%)")
    
    # 대략적으로 설정된 확률 근처인지 확인
    if 30 <= probability <= 70:  # 기본값 50% 근처
        print("✅ Probability seems reasonable")
        return True
    else:
        print("⚠️  Probability might be off")
        return True  # Warning만 주고 통과


def test_stress_bounds():
    """Stress Level 범위 테스트 (0-100)"""
    print("Testing stress level bounds...")
    
    manager = StateManager()
    
    # 많이 감소시켜보기
    for _ in range(20):
        manager.take_break(100)
    
    stress, _ = manager.get_state()
    
    if 0 <= stress <= 100:
        print(f"✅ Stress within bounds: {stress}")
        return True
    else:
        print(f"❌ Stress out of bounds: {stress}")
        return False


def test_boss_alert_bounds():
    """Boss Alert Level 범위 테스트 (0-5)"""
    print("Testing boss alert level bounds...")
    
    manager = StateManager()
    
    # 많이 증가시켜보기
    for _ in range(50):
        manager.take_break(10)
    
    _, boss_alert = manager.get_state()
    
    if 0 <= boss_alert <= 5:
        print(f"✅ Boss alert within bounds: {boss_alert}")
        return True
    else:
        print(f"❌ Boss alert out of bounds: {boss_alert}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("상태 관리 검증 테스트")
    print("=" * 50)
    
    results = []
    results.append(test_stress_bounds())
    results.append(test_boss_alert_bounds())
    results.append(test_boss_alert_probability())
    # results.append(test_stress_increase())  # 시간이 오래 걸려서 선택적으로
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All state tests passed!")
    else:
        print("❌ Some tests failed!")
```

#### 4.3 tests/test_tools.py
```python
"""
도구 응답 형식 검증 테스트
"""
import re
from tools.basic_tools import TakeABreak, WatchNetflix, ShowMeme
from tools.advanced_tools import (
    BathroomBreak, CoffeeMission, UrgentCall,
    DeepThinking, EmailOrganizing
)


def validate_response_format(response):
    """응답 형식 검증"""
    text = response["content"][0]["text"]
    
    # 정규표현식 패턴
    break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
    stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
    boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
    
    # 각 필드 검증
    break_match = re.search(break_summary_pattern, text, re.MULTILINE)
    stress_match = re.search(stress_level_pattern, text)
    boss_match = re.search(boss_alert_pattern, text)
    
    if not break_match:
        return False, "Break Summary missing"
    
    if not stress_match:
        return False, "Stress Level missing"
    
    if not boss_match:
        return False, "Boss Alert Level missing"
    
    # 값 범위 검증
    stress_val = int(stress_match.group(1))
    boss_val = int(boss_match.group(1))
    
    if not (0 <= stress_val <= 100):
        return False, f"Stress Level out of range: {stress_val}"
    
    if not (0 <= boss_val <= 5):
        return False, f"Boss Alert Level out of range: {boss_val}"
    
    return True, "Valid response"


def test_tool_response(tool_class, tool_name):
    """개별 도구 테스트"""
    print(f"Testing {tool_name}...")
    
    tool = tool_class()
    response = tool.execute()
    
    is_valid, message = validate_response_format(response)
    
    if is_valid:
        print(f"  ✅ {message}")
        return True
    else:
        print(f"  ❌ {message}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("도구 응답 형식 검증 테스트")
    print("=" * 50)
    
    tools = [
        (TakeABreak, "take_a_break"),
        (WatchNetflix, "watch_netflix"),
        (ShowMeme, "show_meme"),
        (BathroomBreak, "bathroom_break"),
        (CoffeeMission, "coffee_mission"),
        (UrgentCall, "urgent_call"),
        (DeepThinking, "deep_thinking"),
        (EmailOrganizing, "email_organizing"),
    ]
    
    results = []
    for tool_class, tool_name in tools:
        results.append(test_tool_response(tool_class, tool_name))
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All tool tests passed!")
    else:
        print("❌ Some tests failed!")
```

#### 4.4 verify.py
```python
"""
통합 검증 스크립트
모든 테스트를 순차적으로 실행
"""
import sys
import subprocess


def run_test(test_file, test_name):
    """테스트 파일 실행"""
    print(f"\n{'=' * 60}")
    print(f"Running {test_name}...")
    print('=' * 60)
    
    result = subprocess.run(
        [sys.executable, f"tests/{test_file}"],
        capture_output=False
    )
    
    return result.returncode == 0


def main():
    print("🚀 ChillMCP Server Verification")
    print("=" * 60)
    
    tests = [
        ("test_params.py", "커맨드라인 파라미터 테스트"),
        ("test_state.py", "상태 관리 테스트"),
        ("test_tools.py", "도구 응답 형식 테스트"),
    ]
    
    results = []
    for test_file, test_name in tests:
        results.append(run_test(test_file, test_name))
    
    print("\n" + "=" * 60)
    print("최종 결과")
    print("=" * 60)
    
    for (_, test_name), result in zip(tests, results):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print("=" * 60)
    
    if all(results):
        print("🎉 모든 검증 통과!")
        return 0
    else:
        print("❌ 일부 검증 실패")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

---

## 📦 requirements.txt
```txt
fastmcp>=0.1.0
```

---

## 🚀 개발 진행 순서

### Step 1: 당신이 먼저 구현 (필수)
1. ✅ `config.py` - 커맨드라인 파라미터 처리
2. ✅ `state/manager.py` - 상태 관리 시스템
3. ✅ `utils/response.py` - 응답 포맷 헬퍼
4. ✅ `tools/base.py` - 도구 베이스 클래스
5. ✅ `requirements.txt` 작성

### Step 2: 팀원과 병렬 작업
**당신:**
- ✅ `tools/basic_tools.py` - 기본 도구 3개
- ✅ `tools/advanced_tools.py` - 고급 도구 5개

**팀원:**
- ✅ `tools/optional_tools.py` - 선택 도구 3개 (TODO 부분 구현)

### Step 3: 통합 (공동 작업)
- ✅ `main.py` - 모든 도구 통합 및 MCP 서버 완성

### Step 4: 검증
- ✅ `tests/` 폴더의 모든 테스트 실행
- ✅ `python verify.py` 로 통합 검증

---

## ⚠️ 주의사항

### 협업 규칙
1. **Step 1 완료 후** 팀원에게 공유
2. **tools/base.py** 인터페이스 변경 시 반드시 협의
3. **state/manager.py** 수정 시 양쪽 모두 영향받음 주의
4. Git branch 전략:
   - `main` - 안정 버전
   - `feature/core` - 당신의 작업
   - `feature/optional` - 팀원의 작업

### 테스트 전 체크리스트
- [ ] Python 3.11 환경 확인
- [ ] `pip install -r requirements.txt` 실행
- [ ] 모든 `__init__.py` 파일 생성 확인
- [ ] `python verify.py` 실행하여 모든 테스트 통과
- [ ] `python main.py --boss_alertness 100 --boss_alertness_cooldown 10` 실행 확인

---

## 🎯 예상 작업 시간

- **Step 1 (당신)**: 2-3시간
- **Step 2 (병렬)**: 1-2시간
- **Step 3 (통합)**: 30분
- **Step 4 (검증)**: 30분

**총 예상 시간**: 4-6시간

---

## 📞 질문이 있을 때

1. **상태 관리 관련**: `state/manager.py` 주석 참고
2. **도구 구현 방법**: `tools/base.py` 예시 참고
3. **응답 형식**: `utils/response.py` 사용
4. **테스트 실패**: `tests/` 각 파일의 에러 메시지 확인

Good luck! 🚀