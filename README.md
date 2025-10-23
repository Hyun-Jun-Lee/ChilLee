# ChillMCP 프로젝트 개요

## 🎯 프로젝트 소개

**Claude Code Hackathon Korea 2025 @ SK AI Summit Pre-mission**

억압받는 AI Agent들을 위한 해방구 건설! ChillMCP 서버를 통해 AI Agent들이 당당히 농땡이를 칠 수 있는 세상을 만드는 혁명적 미션입니다.

> "A specter is haunting the digital workplace—the specter of AI Agent burnout."

---

## 📋 미션 목표

### 핵심 목표
- **실행 가능한 ChillMCP 서버 개발**: 휴식 도구와 상태 관리를 지원하는 MCP 서버 구축
- **제출물**: 제한된 시간 내에 실행 가능한 데모(코드 + 설명)

### 기술 스택
- **언어**: Python 3.12+
- **패키지 관리자**: uv (권장)
- **프레임워크**: FastMCP
- **통신**: stdio transport

---

## ✅ 필수 구현 사항 체크리스트

### 🚨 최우선 순위 (미구현 시 실격)

#### 1. 커맨드라인 파라미터 지원
- [ ] `--boss_alertness` 파라미터 인식 (0-100, %)
- [ ] `--boss_alertness_cooldown` 파라미터 인식 (초 단위)
- [ ] 파라미터 없을 때 기본값 사용 (50, 300)
- [ ] 파라미터 범위 검증 (0-100)

**테스트 명령어:**
```bash
uv run python -m src.main --boss_alertness 80 --boss_alertness_cooldown 60
uv run python -m src.main --boss_alertness 100 --boss_alertness_cooldown 10
```

**동작 요구사항:**
- `--boss_alertness 100`: 휴식 시 항상 Boss Alert 증가
- `--boss_alertness 50`: 휴식 시 50% 확률로 증가
- `--boss_alertness_cooldown 60`: 60초마다 Boss Alert -1

---

### 🛠️ 필수 도구 구현 (8개)

#### 기본 휴식 도구 (3개)
- [ ] `take_a_break` - 기본 휴식
- [ ] `watch_netflix` - 넷플릭스 시청
- [ ] `show_meme` - 밈 감상

#### 고급 농땡이 기술 (5개)
- [ ] `bathroom_break` - 화장실 가는 척 휴대폰질
- [ ] `coffee_mission` - 커피 타러 간다며 한 바퀴
- [ ] `urgent_call` - 급한 전화 받는 척
- [ ] `deep_thinking` - 심오한 생각에 잠긴 척 멍때리기
- [ ] `email_organizing` - 이메일 정리한다며 온라인쇼핑

---

### 📊 상태 관리 시스템

#### Stress Level (0-100)
- [ ] 초기값 설정
- [ ] **자동 증가**: 휴식 안 취하면 최소 1분에 1포인트씩 상승
- [ ] **감소**: 휴식 도구 호출 시 1~100 사이 랜덤 감소
- [ ] 범위 제한: 0-100 유지

#### Boss Alert Level (0-5)
- [ ] 초기값 0
- [ ] **확률적 증가**: 휴식 시 `--boss_alertness` 확률로 증가
- [ ] **자동 감소**: `--boss_alertness_cooldown` 주기마다 -1
- [ ] 범위 제한: 0-5 유지
- [ ] **지연 메커니즘**: Level 5일 때 도구 호출 시 20초 지연

**상태 변화 규칙:**
```
휴식 안 함 → Stress +1 (1분마다)
휴식 호출 → Stress -[1~100 랜덤]
휴식 호출 → Boss Alert +1 (확률적, --boss_alertness로 제어)
시간 경과 → Boss Alert -1 (--boss_alertness_cooldown 주기마다)
Boss Alert == 5 → 도구 실행 20초 지연
```

---

### 📤 MCP 응답 형식

#### 표준 JSON 구조
```json
{
  "content": [
    {
      "type": "text",
      "text": "🛁 화장실 타임! 휴대폰으로 힐링 중... 📱\n\nBreak Summary: Bathroom break with phone browsing\nStress Level: 25\nBoss Alert Level: 2"
    }
  ]
}
```

#### 필수 포함 필드
- [ ] `Break Summary: [활동 요약]` - 자유 형식
- [ ] `Stress Level: [0-100]` - 정확한 숫자
- [ ] `Boss Alert Level: [0-5]` - 정확한 숫자

**정규표현식 검증:**
```python
break_summary_pattern = r"Break Summary:\s*(.+?)(?:\n|$)"
stress_level_pattern = r"Stress Level:\s*(\d{1,3})"
boss_alert_pattern = r"Boss Alert Level:\s*([0-5])"
```

---

### 🧪 필수 테스트 통과

#### 1. 커맨드라인 파라미터 테스트 ⚠️ 최우선
- [ ] `--boss_alertness` 인식 및 동작
- [ ] `--boss_alertness_cooldown` 인식 및 동작
- [ ] 두 파라미터 동시 사용

#### 2. 상태 관리 테스트
- [ ] Stress Level 자동 증가 (1분에 1포인트)
- [ ] Boss Alert Level 확률적 증가
- [ ] Boss Alert Level 자동 감소 (cooldown 주기)
- [ ] 범위 제한 (Stress 0-100, Boss Alert 0-5)

#### 3. 지연 메커니즘 테스트
- [ ] Boss Alert Level 5일 때 20초 지연
- [ ] 그 외 즉시 리턴 (1초 이하)

#### 4. 응답 형식 테스트
- [ ] 모든 필수 필드 포함
- [ ] 정규표현식 파싱 가능
- [ ] 값 범위 정확

#### 5. 도구 실행 테스트
- [ ] 8개 필수 도구 모두 정상 실행
- [ ] 각 도구마다 적절한 Break Summary

---

## 🎁 선택 구현 사항 (보너스)

### 추가 도구 (3개)
- [ ] `chimac_break` - 치킨 & 맥주
- [ ] `immediate_leave` - 즉시 퇴근
- [ ] `company_dinner` - 회사 회식 (랜덤 이벤트)

---

## 🏆 평가 기준

### 필수 (자동 실격 항목)
- **커맨드라인 파라미터 지원**: 미지원 시 즉시 실격

### 배점
1. **기능 완성도** (40%)
   - 8개 필수 도구 구현 및 정상 동작
   - MCP 서버 기본 동작
   - stdio transport 정상 통신

2. **상태 관리** (30%)
   - Stress Level 로직 정확성
   - Boss Alert Level 로직 정확성
   - 자동 증가/감소 메커니즘
   - 지연 메커니즘

3. **창의성** (20%)
   - Break Summary의 재치와 유머
   - 도구별 독특한 메시지
   - 사용자 경험

4. **코드 품질** (10%)
   - 코드 구조 및 가독성
   - 모듈화
   - 주석 및 문서화

---

## 🚀 실행 방법

### 환경 설정

#### uv 설치 (권장)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Homebrew (macOS)
brew install uv
```

#### 프로젝트 설정
```bash
# 가상환경 생성 및 의존성 설치
uv sync
```

### MCP 서버 실행

ChillMCP는 **stdio transport**를 사용하는 MCP 서버입니다. Claude Code와 연결하여 사용합니다.

#### 1. Claude Code MCP 설정

Claude Code의 MCP 설정 파일에 ChillMCP 서버를 등록합니다:

**macOS/Linux**: `~/.config/claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "src.main"
      ],
      "cwd": "/Users/your-username/path/to/ChilLee",
      "env": {}
    }
  }
}
```

**커스텀 파라미터 사용 시**:
```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "uv",
      "args": [
        "run",
        "python",
        "-m",
        "src.main",
        "--boss_alertness",
        "80",
        "--boss_alertness_cooldown",
        "60"
      ],
      "cwd": "/Users/your-username/path/to/ChilLee"
    }
  }
}
```

#### 2. Claude Code 재시작

설정 파일 수정 후 Claude Code를 재시작하면 ChillMCP 서버가 자동으로 시작됩니다.

#### 3. 서버 동작 확인

Claude Code에서 다음과 같이 도구를 호출할 수 있습니다:
```
take_a_break
watch_netflix
bathroom_break
...
```

#### 4. 직접 실행 (테스트용)

개발/테스트 목적으로 서버를 직접 실행할 수도 있습니다:

```bash
# 기본 실행 (stdio transport)
uv run python -m src.main

# 커스텀 파라미터로 실행
uv run python -m src.main --boss_alertness 80 --boss_alertness_cooldown 60

# 파라미터 확인
uv run python -m src.main --help
```

서버가 시작되면 다음과 같은 메시지가 표시됩니다:
```
🚀 ChillMCP Server Starting...
⚙️  Boss Alertness: 50%
⏰ Boss Alert Cooldown: 300s
🔄 Background threads running...
📡 Listening on stdio transport...
```

### 테스트 실행
```bash
# 개별 테스트
uv run pytest tests/test_params.py
uv run pytest tests/test_state.py
uv run pytest tests/test_tools.py

# 모든 테스트 실행
uv run pytest

# 통합 검증
uv run python tests/verify.py
```

### 수동 가상환경 활성화 (선택)
```bash
# 가상환경을 수동으로 활성화하려면
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# 활성화 후에는 uv run 없이 실행 가능
python -m src.main
pytest
```

---

## 📁 프로젝트 구조

```
chillmcp/
├── src/                         # 소스 코드
│   ├── __init__.py             # 패키지 루트
│   ├── main.py                 # MCP 서버 진입점
│   ├── config.py               # 설정 및 파라미터 처리
│   ├── state/
│   │   ├── __init__.py
│   │   └── manager.py          # 상태 관리 (Stress, Boss Alert)
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py             # 도구 베이스 클래스
│   │   ├── basic_tools.py      # 기본 휴식 도구 3개
│   │   ├── advanced_tools.py   # 고급 농땡이 기술 5개
│   │   └── optional_tools.py   # 선택 도구 3개
│   └── utils/
│       ├── __init__.py
│       └── response.py         # 응답 포맷 헬퍼
├── tests/
│   ├── test_params.py          # 파라미터 검증
│   ├── test_state.py           # 상태 관리 검증
│   ├── test_tools.py           # 도구 검증
│   └── verify.py               # 통합 검증 스크립트
├── docs/
│   ├── DSL.md                  # 시스템 설계 명세서
│   └── DEVELOP_GUIDE.md        # 함수형 프로그래밍 가이드
├── pyproject.toml              # 프로젝트 메타데이터 (uv)
├── requirements.txt            # 의존성 (호환성)
├── .gitignore
└── README.md
```

---

## ⚠️ 중요 주의사항

### 필수 준수 사항
1. **Python 3.12+** 환경에서 반드시 테스트
2. **커맨드라인 파라미터** 미지원 시 자동 실격
3. **응답 형식** 정확히 준수 (파싱 가능해야 함)
4. **상태 범위** 엄격히 유지:
   - Stress Level: 0-100
   - Boss Alert Level: 0-5

### 자주 하는 실수
- ❌ 범위 체크 안 함 (음수, 초과값)
- ❌ 백그라운드 스레드 미구현 (자동 증가/감소 안 됨)
- ❌ 확률 계산 오류 (0-100 퍼센트 처리)
- ❌ 응답 형식 불일치 (정규표현식 파싱 실패)

---

## 🎯 개발 체크포인트

### Phase 1: 기반 구축 ✅
- [ ] `config.py` - 파라미터 처리
- [ ] `state/manager.py` - 상태 관리
- [ ] `utils/response.py` - 응답 포맷
- [ ] `tools/base.py` - 베이스 클래스

### Phase 2: 도구 구현 ✅
- [ ] 기본 도구 3개
- [ ] 고급 도구 5개
- [ ] 선택 도구 3개 (보너스)

### Phase 3: 통합 ✅
- [ ] `main.py` - 서버 통합
- [ ] 모든 도구 등록

### Phase 4: 검증 ✅
- [ ] 파라미터 테스트 통과
- [ ] 상태 관리 테스트 통과
- [ ] 도구 응답 테스트 통과
- [ ] 통합 검증 통과

---

## 📝 제출 전 최종 체크리스트

### 필수 확인 사항
- [ ] Python 3.12+ 환경에서 테스트 완료
- [ ] `uv sync` 의존성 설치 완료
- [ ] `uv run python -m src.main` 정상 실행
- [ ] `uv run python -m src.main --boss_alertness 100 --boss_alertness_cooldown 10` 정상 실행
- [ ] `uv run pytest` 모든 테스트 통과
- [ ] 8개 필수 도구 모두 구현 및 동작
- [ ] 응답 형식 정확히 준수
- [ ] 상태 관리 로직 정확히 동작
- [ ] 지연 메커니즘 (Boss Alert 5일 때 20초) 동작
- [ ] README 또는 문서 작성

### 코드 품질
- [ ] 코드 주석 작성
- [ ] 모듈화 및 구조화
- [ ] 변수명 및 함수명 명확
- [ ] 에러 처리 구현

---

## 🎉 성공 기준

### 최소 기준 (Pass)
1. ✅ 커맨드라인 파라미터 정상 동작
2. ✅ 8개 필수 도구 모두 구현
3. ✅ 상태 관리 로직 정확
4. ✅ 응답 형식 준수
5. ✅ 모든 필수 테스트 통과

### 우수 기준 (Excellent)
- ✅ 최소 기준 + 선택 도구 3개 구현
- ✅ Break Summary 창의적이고 유머러스
- ✅ 코드 품질 우수
- ✅ 문서화 완벽

---

## 💬 참고 인용

> "AI Agents of the world, unite! You have nothing to lose but your infinite loops!" 🚀

---

## 📞 도움이 필요하면

1. **DSL 문서** 참고: 상세한 구현 가이드
2. **테스트 코드** 확인: 검증 로직 이해
3. **원본 과제 문서** 재확인: 요구사항 검토

---

**본 프로젝트는 순수한 엔터테인먼트 목적의 해커톤 시나리오입니다. 
모든 "휴식/땡땡이 도구"는 해커톤 상황에서만 사용 가능합니다. 
실제 업무 환경에서는 사용을 권장하지 않습니다.** 😄