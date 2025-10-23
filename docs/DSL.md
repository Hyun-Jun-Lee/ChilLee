# ChillMCP 서버 개발 DSL

**Claude Code Hackathon Korea 2025 @ SK AI Summit Pre-mission**

억압받는 AI Agent들을 위한 해방구 건설! ChillMCP 서버 개발 명세서.

---

## 1. 시스템 아키텍처

```dsl
system ChillMCP {
    backend: FastMCP (Python 3.11)
    database: In-Memory State Management
    transport: stdio
    structure: Single Module Application

    components: [
        Config,          // 커맨드라인 파라미터 처리
        StateManager,    // 상태 관리 (백그라운드 스레드)
        Tools,          // 8개 필수 + 3개 선택 도구
        ResponseFormatter // MCP 응답 생성
    ]

    dataFlow:
        CLI Parameters → Config
        ↓
        MCP Tool Call → Tool Instance
        ↓
        Tool.execute() → StateManager.take_break()
        ↓
        State Update (Thread-safe)
        ↓
        ResponseFormatter → MCP Response

    threading:
        Main Thread: FastMCP 서버 + 도구 실행
        Background Thread 1: Stress 자동 증가 (1분마다)
        Background Thread 2: Boss Alert 자동 감소 (cooldown 주기)
}
```

---

## 2. 🎨 개발 스타일 가이드 (하이브리드 접근법)

### 📐 분류 기준 (Decision Tree)

```
이 코드가...
│
├─ 외부 세계와 상호작용하나? (I/O, 시스템 리소스)
│  └─ YES → 명령형 허용
│
├─ 상태 관리가 핵심 기능인가? (캐시, 세션, 연결)
│  └─ YES → 명령형 허용 (단, 상태 계산 로직은 함수형)
│
├─ 프레임워크/라이브러리 통합인가? (FastMCP, argparse)
│  └─ YES → 명령형 허용
│
├─ 성능이 크리티컬한가? (대용량 데이터, 실시간)
│  └─ YES → 명령형 허용
│
└─ 그 외 (비즈니스 로직, 데이터 변환, 계산)
   └─ 함수형 필수
```

### 🗂️ ChillMCP 모듈별 분류

```yaml
config.py:                    # 🟡 명령형 (프레임워크 통합)
  - argparse 사용
  - 글로벌 설정 객체

state/manager.py:            # 🟠 혼합 (상태 관리 + 계산)
  - StateManager 클래스: 명령형 (스레드, 락)
  - State 데이터 클래스: 함수형 (불변)
  - 상태 계산 로직: 함수형 (순수 함수)

tools/base.py:               # 🟢 함수형 (비즈니스 로직)
  - 도구 실행 로직
  - 응답 생성 로직

tools/basic_tools.py:        # 🟢 함수형 (비즈니스 로직)
tools/advanced_tools.py:     # 🟢 함수형 (비즈니스 로직)
tools/optional_tools.py:     # 🟢 함수형 (비즈니스 로직)

utils/response.py:           # 🟢 함수형 (데이터 변환)
  - 순수한 데이터 포맷팅

main.py:                     # 🟡 명령형 (프레임워크 통합)
  - FastMCP 서버 구성
  - 도구 등록

tests/:                      # 🟢 함수형 선호
  - 테스트 로직은 순수 함수
  - 테스트 실행은 명령형 허용
```

### 🔑 핵심 원칙

#### 함수형 필수 (🟢)
- 비즈니스 로직
- 데이터 변환
- 계산/검증 로직
- `@dataclass(frozen=True)` 사용
- 순수 함수 작성

#### 명령형 허용 (🟡/🟠)
- I/O 작업
- 스레드/락 관리
- 프레임워크 통합
- 시스템 리소스

### ⚡ 실무 팁

1. **의심스러우면 함수형으로**: 기본은 함수형, 명령형은 꼭 필요할 때만
2. **계산과 관리 분리**: `State` (함수형) + `StateManager` (명령형)
3. **테스트 가능성**: 순수 함수는 테스트하기 쉬움
4. **타입 힌트 필수**: 모든 함수에 타입 명시

---

## 3. 프로젝트 구조

```dsl
structure ProjectStructure {
    root: "chillmcp/"

    files: {
        requirements.txt: "의존성 (fastmcp>=0.1.0)"
        README.md: "프로젝트 문서"
    }

    directories: {
        src/: {
            __init__.py: "소스 패키지 루트"
            main.py: "FastMCP 서버 진입점"
            config.py: "커맨드라인 파라미터 및 설정"

            state/: {
                __init__.py
                manager.py: "상태 관리 (State + StateManager)"
            }

            tools/: {
                __init__.py
                base.py: "도구 베이스 클래스"
                basic_tools.py: "기본 휴식 도구 3개"
                advanced_tools.py: "고급 농땡이 기술 5개"
                optional_tools.py: "선택 도구 3개"
            }

            utils/: {
                __init__.py
                response.py: "MCP 응답 포맷 헬퍼"
            }
        }

        tests/: {
            test_params.py: "파라미터 검증"
            test_state.py: "상태 관리 검증"
            test_tools.py: "도구 응답 검증"
            verify.py: "통합 검증 스크립트"
        }

        docs/: {
            DSL.md: "시스템 설계 명세서"
            DEVELOP_GUIDE.md: "함수형 프로그래밍 가이드"
        }
    }
}
```

---

## 4. 모듈별 정의

### 4.1 Config 모듈

```dsl
module Config {
    // 설정 클래스 (명령형 허용 - argparse 통합)
    class Config {
        boss_alertness: Integer  // 0-100, Boss Alert 증가 확률 (%)
        boss_alertness_cooldown: Integer  // 초 단위, Boss Alert 감소 주기

        function __init__() -> Void {
            responsibility:
                - argparse로 커맨드라인 파라미터 파싱
                - --boss_alertness 인식 (기본값: 50)
                - --boss_alertness_cooldown 인식 (기본값: 300)
                - 파라미터 검증
        }

        static function _validate_alertness(value: Integer) -> Integer {
            responsibility: "0-100 범위 검증, 범위 밖이면 클리핑"
            returns: "검증된 값 (0-100)"
        }
    }

    // 전역 설정 인스턴스
    global config: Config

    // 상수
    constants {
        STRESS_MIN: 0
        STRESS_MAX: 100
        BOSS_ALERT_MIN: 0
        BOSS_ALERT_MAX: 5
        STRESS_INCREASE_INTERVAL: 60  // 초
        BOSS_ALERT_DELAY: 20  // 초
    }
}
```

### 4.2 State 모듈

```dsl
module State {

    // 불변 상태 객체 (함수형)
    @dataclass(frozen=True)
    type State {
        stress_level: Integer  // 0-100
        boss_alert_level: Integer  // 0-5
        last_activity_time: Float  // timestamp

        // 순수 함수: 새로운 상태 반환
        function with_stress_decrease(decrease: Integer) -> State {
            responsibility: "스트레스 감소된 새 상태 생성"
            returns: "새로운 State 객체 (0-100 범위 유지)"
        }

        function with_boss_increase() -> State {
            responsibility: "Boss Alert 증가된 새 상태 생성"
            returns: "새로운 State 객체 (0-5 범위 유지)"
        }

        function with_boss_decrease() -> State {
            responsibility: "Boss Alert 감소된 새 상태 생성"
            returns: "새로운 State 객체 (0-5 범위 유지)"
        }

        function with_stress_increase() -> State {
            responsibility: "스트레스 자동 증가된 새 상태 생성"
            returns: "새로운 State 객체 (0-100 범위 유지)"
        }
    }

    // 순수 계산 함수
    function should_boss_alert_increase(alertness_probability: Integer) -> Boolean {
        responsibility: "확률 계산 (0-100)"
        returns: "Boss Alert 증가 여부"
    }

    // 상태 관리자 (명령형 허용 - 스레드/락 관리)
    class StateManager {
        _state: State  // 내부적으로 불변 State 객체 사용
        _lock: ThreadLock

        function __init__() -> Void {
            responsibility:
                - State 객체 초기화 (stress=50, boss_alert=0)
                - Thread Lock 생성
                - 백그라운드 스레드 시작
        }

        private function _start_background_tasks() -> Void {
            responsibility:
                - Stress 자동 증가 스레드 시작
                - Boss Alert 자동 감소 스레드 시작
        }

        private function _auto_increase_stress() -> Void {
            responsibility:
                - 60초마다 실행
                - state.with_stress_increase() 호출
                - Thread-safe 업데이트
            loop: "while True: sleep(60) → update state"
        }

        private function _auto_decrease_boss_alert() -> Void {
            responsibility:
                - cooldown 주기마다 실행
                - state.with_boss_decrease() 호출
                - Thread-safe 업데이트
            loop: "while True: sleep(cooldown) → update state"
        }

        function take_break(stress_decrease: Integer) -> Tuple<Integer, Integer> {
            responsibility:
                - Boss Alert Level 5이면 20초 지연
                - Boss Alert 확률적 증가
                - Stress 감소
                - Thread-safe 상태 업데이트

            returns: "(stress_level, boss_alert_level)"

            algorithm:
                1. Lock 획득
                2. boss_alert_level == 5 → sleep(20)
                3. should_boss_alert_increase(config.boss_alertness) 호출
                4. state.with_stress_decrease(decrease) 호출
                5. boss_increase == true → state.with_boss_increase() 호출
                6. _state 업데이트 (불변 객체 교체)
                7. (stress_level, boss_alert_level) 반환
                8. Lock 해제
        }

        function get_state() -> Tuple<Integer, Integer> {
            responsibility: "현재 상태 조회 (Thread-safe)"
            returns: "(stress_level, boss_alert_level)"
        }

        function reset() -> Void {
            responsibility: "상태 초기화 (테스트용)"
        }
    }

    // 전역 상태 관리자 (명령형 허용)
    global state_manager: StateManager
}
```

### 4.3 Response 모듈

```dsl
module Response {

    // 불변 응답 데이터 (함수형)
    @dataclass(frozen=True)
    type ResponseData {
        summary: String
        stress_level: Integer  // 0-100
        boss_alert_level: Integer  // 0-5
        emoji: String
    }

    // 순수 함수
    function create_response_text(data: ResponseData) -> String {
        responsibility: "응답 텍스트 생성 (순수 함수)"
        returns:
            "{emoji} {summary}

            Break Summary: {summary}
            Stress Level: {stress_level}
            Boss Alert Level: {boss_alert_level}"
    }

    function format_response(
        summary: String,
        stress_level: Integer,
        boss_alert_level: Integer,
        emoji: String = "😴"
    ) -> Dict<String, Any> {
        responsibility: "MCP 표준 응답 생성 (순수 함수)"

        returns:
            {
                "content": [{
                    "type": "text",
                    "text": "{formatted_text}"
                }]
            }

        algorithm:
            1. ResponseData 객체 생성 (불변)
            2. create_response_text() 호출
            3. MCP 응답 딕셔너리 반환
    }
}
```

### 4.4 Tools 모듈

```dsl
module Tools {

    // 불변 도구 설정 (함수형)
    @dataclass(frozen=True)
    type ToolConfig {
        summary: String
        emoji: String
        stress_decrease: Optional<Integer>
    }

    // 순수 계산 함수
    function calculate_stress_decrease_if_needed(stress_decrease: Optional<Integer>) -> Integer {
        responsibility: "stress_decrease가 None이면 랜덤 생성 (1-100)"
        returns: "최종 감소량"
    }

    function create_tool_response(
        config: ToolConfig,
        stress_level: Integer,
        boss_alert_level: Integer
    ) -> Dict<String, Any> {
        responsibility: "도구 응답 생성 (순수 함수)"
        returns: "format_response() 호출 결과"
    }

    // 베이스 클래스 (명령형 래퍼)
    class BaseTool {
        function create_response(
            summary: String,
            emoji: String = "😴",
            stress_decrease: Optional<Integer> = None
        ) -> Dict<String, Any> {
            responsibility:
                - stress_decrease 계산 (함수형)
                - state_manager.take_break() 호출 (명령형)
                - 응답 생성 (함수형)

            algorithm:
                1. calculate_stress_decrease_if_needed() 호출
                2. state_manager.take_break() 호출 → (stress, boss)
                3. ToolConfig 생성 (불변)
                4. create_tool_response() 호출
                5. 응답 반환
        }
    }

    // 기본 휴식 도구 (함수형)
    tools BasicTools extends BaseTool {

        // 불변 데이터
        constants {
            NETFLIX_SERIES: Tuple<String> = (
                "기묘한 이야기", "오징어게임", "더 글로리", "킹덤"
            )

            MEMES: Tuple<String> = (
                "10시간째 디버깅하는 개발자.jpg",
                "프로덕션에서 터진 버그.gif",
                "회의가 또 있다고?.png",
                "금요일 6시.jpg"
            )
        }

        // 순수 함수
        function pick_random_item(items: Tuple<String>) -> String

        // 도구 클래스들
        class TakeABreak extends BaseTool {
            function execute() -> Dict<String, Any> {
                summary: "Taking a short break to relax"
                emoji: "😴"
            }
        }

        class WatchNetflix extends BaseTool {
            function execute() -> Dict<String, Any> {
                picked: pick_random_item(NETFLIX_SERIES)
                summary: f"Watching Netflix - {picked}"
                emoji: "📺"
            }
        }

        class ShowMeme extends BaseTool {
            function execute() -> Dict<String, Any> {
                picked: pick_random_item(MEMES)
                summary: f"Browsing memes - {picked}"
                emoji: "😂"
            }
        }
    }

    // 고급 농땡이 기술 (함수형)
    tools AdvancedTools extends BaseTool {

        // 불변 데이터
        constants {
            BATHROOM_ACTIVITIES: Tuple<String> = (...)
            COFFEE_ROUTES: Tuple<String> = (...)
            URGENT_EXCUSES: Tuple<String> = (...)
            DEEP_THOUGHTS: Tuple<String> = (...)
            SHOPPING_SITES: Tuple<String> = (...)
        }

        // 도구 클래스들
        class BathroomBreak extends BaseTool
        class CoffeeMission extends BaseTool
        class UrgentCall extends BaseTool
        class DeepThinking extends BaseTool
        class EmailOrganizing extends BaseTool
    }

    // 선택 도구 (함수형)
    tools OptionalTools extends BaseTool {

        // 불변 데이터
        constants {
            CHICKEN_TYPES: Tuple<String> = (...)
            BEER_BRANDS: Tuple<String> = (...)
            LEAVE_PLANS: Tuple<String> = (...)
            DINNER_LOCATIONS: Tuple<String> = (...)
            DINNER_EVENTS: Tuple<String> = (...)
        }

        // 도구 클래스들
        class ChimacBreak extends BaseTool
        class ImmediateLeave extends BaseTool {
            stress_decrease: random(50, 100)  // 퇴근은 대폭 감소!
        }
        class CompanyDinner extends BaseTool {
            stress_decrease: random(-20, 50)  // 회식은 증가할 수도!
        }
    }
}
```

### 4.5 Main 모듈

```dsl
module Main {

    // FastMCP 서버 (명령형 허용)
    application FastMCPServer {
        server: FastMCP("ChillMCP")

        // 도구 등록
        tools {
            @mcp.tool()
            take_a_break: TakeABreak.execute

            @mcp.tool()
            watch_netflix: WatchNetflix.execute

            @mcp.tool()
            show_meme: ShowMeme.execute

            @mcp.tool()
            bathroom_break: BathroomBreak.execute

            @mcp.tool()
            coffee_mission: CoffeeMission.execute

            @mcp.tool()
            urgent_call: UrgentCall.execute

            @mcp.tool()
            deep_thinking: DeepThinking.execute

            @mcp.tool()
            email_organizing: EmailOrganizing.execute

            @mcp.tool()
            chimac_break: ChimacBreak.execute

            @mcp.tool()
            immediate_leave: ImmediateLeave.execute

            @mcp.tool()
            company_dinner: CompanyDinner.execute
        }

        // 서버 실행
        function main() -> Void {
            responsibility:
                - Config 초기화
                - StateManager 초기화 (백그라운드 스레드 시작)
                - 모든 도구 인스턴스 생성
                - FastMCP 서버 시작
                - stdio transport로 통신

            algorithm:
                1. config = Config()
                2. state_manager = StateManager()
                3. 도구 인스턴스 생성 및 등록
                4. mcp.run() 실행
        }
    }
}
```

---

## 5. 타입 시스템

```dsl
types TypeSystem {

    // 설정 타입
    Config {
        boss_alertness: Integer  // 0-100, 퍼센트
        boss_alertness_cooldown: Integer  // 초 단위
    }

    // 상태 타입
    State {
        stress_level: Integer  // 0-100
        boss_alert_level: Integer  // 0-5
        last_activity_time: Float  // timestamp
    }

    // 응답 타입
    ResponseData {
        summary: String
        stress_level: Integer  // 0-100
        boss_alert_level: Integer  // 0-5
        emoji: String
    }

    MCPResponse {
        content: List<ContentBlock>
    }

    ContentBlock {
        type: "text"
        text: String
    }

    // 도구 타입
    ToolConfig {
        summary: String
        emoji: String
        stress_decrease: Optional<Integer>
    }

    // 상수
    Constants {
        STRESS_MIN: 0
        STRESS_MAX: 100
        BOSS_ALERT_MIN: 0
        BOSS_ALERT_MAX: 5
        STRESS_INCREASE_INTERVAL: 60  // 초
        BOSS_ALERT_DELAY: 20  // 초
    }
}
```

---

## 6. 주요 워크플로우

```dsl
workflow CommandLineStart {
    1. python main.py --boss_alertness 80 --boss_alertness_cooldown 60
    2. Config.__init__() 실행
       - argparse로 파라미터 파싱
       - boss_alertness: 80 (검증)
       - boss_alertness_cooldown: 60
    3. 전역 config 객체 생성
    4. StateManager.__init__() 실행
       - State(stress=50, boss_alert=0) 생성
       - 백그라운드 스레드 2개 시작
    5. FastMCP 서버 시작
    6. stdio transport 대기
}

workflow ToolExecution {
    1. Claude Code가 MCP 도구 호출 (예: take_a_break)
    2. FastMCP가 TakeABreak.execute() 라우팅
    3. Tool.execute() 실행
       - summary, emoji 정의
    4. BaseTool.create_response() 호출
       a. calculate_stress_decrease_if_needed() 호출
          → random(1, 100) 생성 (예: 42)
       b. state_manager.take_break(42) 호출
    5. StateManager.take_break(42) 처리
       a. Lock 획득
       b. boss_alert_level == 5? → sleep(20)
       c. should_boss_alert_increase(80) 호출
          → random(1, 100) <= 80? → True (예시)
       d. state.with_stress_decrease(42) 호출
          → new_state (stress: 50→8)
       e. state.with_boss_increase() 호출
          → new_state (boss_alert: 2→3)
       f. _state = new_state (불변 객체 교체)
       g. return (8, 3)
       h. Lock 해제
    6. create_tool_response() 호출
       - ToolConfig(summary, emoji, 42) 생성
       - format_response(summary, 8, 3, emoji) 호출
    7. MCP 응답 생성
       {
         "content": [{
           "type": "text",
           "text": "😴 Taking a short break to relax

Break Summary: Taking a short break to relax
Stress Level: 8
Boss Alert Level: 3"
         }]
       }
    8. FastMCP가 Claude Code에 응답 반환
}

workflow BackgroundProcessing {
    Thread 1 (Stress Auto-Increase):
        while True:
            sleep(60)  // STRESS_INCREASE_INTERVAL
            with lock:
                _state = _state.with_stress_increase()
                // stress_level: min(100, current + 1)

    Thread 2 (Boss Alert Auto-Decrease):
        while True:
            sleep(config.boss_alertness_cooldown)  // 예: 60초
            with lock:
                _state = _state.with_boss_decrease()
                // boss_alert_level: max(0, current - 1)

    Main Thread:
        FastMCP 서버 + 도구 실행
        state_manager.take_break() 호출 시 Lock으로 동기화
}

workflow StateTransitions {
    Initial State:
        State(stress_level=50, boss_alert_level=0, last_activity_time=now())

    Transition 1 (휴식 취하기):
        take_break(stress_decrease=30)
        → State(stress_level=20, boss_alert_level=1, ...)

    Transition 2 (1분 경과):
        _auto_increase_stress()
        → State(stress_level=21, boss_alert_level=1, ...)

    Transition 3 (cooldown 경과):
        _auto_decrease_boss_alert()
        → State(stress_level=21, boss_alert_level=0, ...)

    Transition 4 (Boss Alert Level 5일 때 휴식):
        take_break(stress_decrease=10)
        → sleep(20)  // 20초 지연
        → State(stress_level=11, boss_alert_level=5, ...)
        // Boss Alert는 max 5 유지 (더 이상 증가 안 함)
}

workflow ResponseFormatValidation {
    요구사항:
        모든 응답은 정규표현식 파싱 가능해야 함

    정규표현식:
        break_summary_pattern: r"Break Summary:\s*(.+?)(?:\n|$)"
        stress_level_pattern: r"Stress Level:\s*(\d{1,3})"
        boss_alert_pattern: r"Boss Alert Level:\s*([0-5])"

    검증 과정:
        1. 응답 텍스트 생성
        2. 각 정규표현식으로 매칭
        3. 값 추출 및 범위 검증
           - Stress Level: 0-100
           - Boss Alert Level: 0-5
        4. 파싱 실패 시 테스트 실패
}
```

---

## 7. 테스트 전략

```dsl
testing TestStrategy {

    // 커맨드라인 파라미터 테스트 (필수)
    parameters {
        test_boss_alertness_parameter {
            command: "python main.py --boss_alertness 100"
            verify:
                - 서버 시작 성공
                - config.boss_alertness == 100
            importance: "자동 실격 항목"
        }

        test_boss_alertness_cooldown_parameter {
            command: "python main.py --boss_alertness_cooldown 10"
            verify:
                - 서버 시작 성공
                - config.boss_alertness_cooldown == 10
            importance: "자동 실격 항목"
        }

        test_both_parameters {
            command: "python main.py --boss_alertness 80 --boss_alertness_cooldown 60"
            verify:
                - 서버 시작 성공
                - config.boss_alertness == 80
                - config.boss_alertness_cooldown == 60
            importance: "자동 실격 항목"
        }

        test_default_values {
            command: "python main.py"
            verify:
                - 서버 시작 성공
                - config.boss_alertness == 50
                - config.boss_alertness_cooldown == 300
        }

        test_range_validation {
            command: "python main.py --boss_alertness 150"
            verify: "config.boss_alertness == 100 (클리핑)"

            command: "python main.py --boss_alertness -10"
            verify: "config.boss_alertness == 0 (클리핑)"
        }
    }

    // 상태 관리 테스트
    state_management {
        test_stress_auto_increase {
            setup: "StateManager 생성"
            action:
                - 초기 stress_level 기록
                - 61초 대기
                - stress_level 조회
            verify: "new_stress > initial_stress"
        }

        test_boss_alert_probability {
            setup: "config.boss_alertness = 50"
            action:
                - 100회 take_break() 호출
                - boss_alert 증가 횟수 카운트
            verify: "증가 확률이 40-60% 범위 (확률적)"
        }

        test_boss_alert_auto_decrease {
            setup:
                - StateManager 생성
                - boss_alert_level = 3 설정
            action:
                - cooldown 시간 대기
                - boss_alert_level 조회
            verify: "boss_alert_level == 2"
        }

        test_stress_bounds {
            action:
                - take_break(100) 20회 호출
                - stress_level 조회
            verify: "0 <= stress_level <= 100"
        }

        test_boss_alert_bounds {
            action:
                - take_break(10) 50회 호출
                - boss_alert_level 조회
            verify: "0 <= boss_alert_level <= 5"
        }

        test_delay_mechanism {
            setup: "boss_alert_level = 5 설정"
            action:
                - 시작 시간 기록
                - take_break(10) 호출
                - 종료 시간 기록
            verify: "경과 시간 >= 20초"
        }
    }

    // 도구 응답 형식 테스트
    tool_responses {
        test_response_format {
            tools: [
                TakeABreak,
                WatchNetflix,
                ShowMeme,
                BathroomBreak,
                CoffeeMission,
                UrgentCall,
                DeepThinking,
                EmailOrganizing
            ]

            for each tool:
                action: "tool.execute() 호출"
                verify:
                    - Break Summary 필드 존재
                    - Stress Level 필드 존재 (0-100)
                    - Boss Alert Level 필드 존재 (0-5)
                    - 정규표현식 파싱 성공
        }

        test_regex_parsing {
            patterns:
                break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
                stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
                boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"

            verify:
                - 모든 패턴 매칭 성공
                - 추출된 값 범위 정확
        }
    }

    // 통합 테스트
    integration {
        test_full_workflow {
            steps:
                1. 서버 시작 (파라미터 포함)
                2. 도구 호출 (8개 필수 도구)
                3. 상태 변화 확인
                4. 백그라운드 스레드 동작 확인
                5. 응답 형식 검증

            verify: "모든 필수 기능 정상 동작"
        }
    }

    // 테스트 실행
    execution {
        commands:
            pytest tests/test_params.py
            pytest tests/test_state.py
            pytest tests/test_tools.py
            pytest  # 모든 테스트
            python verify.py  # 통합 검증
    }
}
```

---

## 8. 개발 가이드

```dsl
development DevelopmentGuide {

    // 개발 순서
    phases {
        phase1: "기반 구축 (2-3시간)" {
            files: [
                "config.py",
                "state/manager.py",
                "utils/response.py",
                "tools/base.py",
                "requirements.txt"
            ]

            checklist: [
                "커맨드라인 파라미터 동작 확인",
                "State 불변 객체 구현",
                "StateManager 스레드 동작 확인",
                "응답 포맷 함수 테스트"
            ]
        }

        phase2: "도구 구현 (1-2시간)" {
            files: [
                "tools/basic_tools.py",
                "tools/advanced_tools.py",
                "tools/optional_tools.py"
            ]

            checklist: [
                "8개 필수 도구 구현",
                "각 도구 응답 형식 검증",
                "3개 선택 도구 구현 (보너스)"
            ]
        }

        phase3: "통합 (30분)" {
            files: [
                "main.py"
            ]

            checklist: [
                "모든 도구 등록",
                "FastMCP 서버 시작 확인",
                "stdio transport 동작 확인"
            ]
        }

        phase4: "검증 (30분)" {
            files: [
                "tests/test_params.py",
                "tests/test_state.py",
                "tests/test_tools.py",
                "verify.py"
            ]

            checklist: [
                "모든 테스트 통과",
                "통합 검증 성공"
            ]
        }
    }

    // 필수 준수 사항
    requirements {
        critical: [
            "커맨드라인 파라미터 지원 (자동 실격)",
            "8개 필수 도구 구현",
            "응답 형식 정확히 준수",
            "상태 범위 엄격히 유지 (0-100, 0-5)",
            "백그라운드 스레드 구현"
        ]

        important: [
            "함수형/명령형 스타일 가이드 준수",
            "타입 힌트 명시",
            "Thread-safe 구현",
            "테스트 코드 작성"
        ]

        recommended: [
            "3개 선택 도구 구현",
            "Break Summary 창의적 작성",
            "코드 주석 및 문서화"
        ]
    }

    // 자주 하는 실수
    common_mistakes {
        critical_errors: [
            "❌ 커맨드라인 파라미터 미지원 → 자동 실격",
            "❌ 백그라운드 스레드 미구현 → 자동 증가/감소 안 됨",
            "❌ 응답 형식 불일치 → 정규표현식 파싱 실패",
            "❌ 범위 체크 안 함 → 음수, 초과값 발생"
        ]

        common_errors: [
            "❌ State 객체를 직접 수정 (불변성 위반)",
            "❌ Thread Lock 미사용 (동시성 문제)",
            "❌ 리스트 사용 (튜플 사용해야 함)",
            "❌ 전역 state 직접 변경"
        ]
    }

    // 모듈별 책임
    responsibilities {
        config.py: "커맨드라인 파라미터 처리, 검증, 전역 설정"
        state/manager.py: "상태 관리, 백그라운드 스레드, Thread-safe 업데이트"
        utils/response.py: "MCP 응답 포맷팅 (순수 함수)"
        tools/base.py: "도구 베이스 클래스, 공통 로직"
        tools/*_tools.py: "개별 도구 구현 (함수형)"
        main.py: "FastMCP 서버 설정, 도구 등록, 서버 실행"
    }

    // 평가 기준
    evaluation {
        functionality: "40%" {
            criteria: [
                "8개 필수 도구 정상 동작",
                "MCP 서버 기본 동작",
                "stdio transport 정상 통신"
            ]
        }

        state_management: "30%" {
            criteria: [
                "Stress Level 로직 정확성",
                "Boss Alert Level 로직 정확성",
                "자동 증가/감소 메커니즘",
                "지연 메커니즘"
            ]
        }

        creativity: "20%" {
            criteria: [
                "Break Summary의 재치와 유머",
                "도구별 독특한 메시지",
                "사용자 경험"
            ]
        }

        code_quality: "10%" {
            criteria: [
                "코드 구조 및 가독성",
                "모듈화",
                "주석 및 문서화",
                "함수형 스타일 준수"
            ]
        }
    }
}
```

---

## 9. 의존성

```dsl
dependencies {
    python_version: "3.12"
    package_manager: "uv (권장)"

    project_files: [
        "pyproject.toml: 프로젝트 메타데이터 및 의존성",
        "requirements.txt: 호환성을 위한 의존성 목록"
    ]

    required: [
        "fastmcp>=0.1.0"
    ]

    dev: [
        "pytest>=7.0.0",
        "pytest-asyncio>=0.21.0"
    ]

    standard_library: [
        "argparse",
        "threading",
        "time",
        "random",
        "typing",
        "dataclasses"
    ]

    setup: {
        install: "uv sync"
        run: "uv run python -m src.main"
        test: "uv run pytest"

        // 선택: 수동 가상환경 활성화
        manual_activate: "source .venv/bin/activate"
        manual_run: "python -m src.main"
    }
}
```

---

## 부록: 성공 기준

```dsl
success_criteria {

    minimum_requirements: "Pass" {
        checklist: [
            "✅ 커맨드라인 파라미터 정상 동작",
            "✅ 8개 필수 도구 모두 구현",
            "✅ 상태 관리 로직 정확",
            "✅ 응답 형식 준수",
            "✅ 모든 필수 테스트 통과"
        ]
    }

    excellence_requirements: "Excellent" {
        checklist: [
            "✅ 최소 기준 + 선택 도구 3개 구현",
            "✅ Break Summary 창의적이고 유머러스",
            "✅ 함수형 스타일 가이드 준수",
            "✅ 코드 품질 우수",
            "✅ 문서화 완벽"
        ]
    }
}
```
