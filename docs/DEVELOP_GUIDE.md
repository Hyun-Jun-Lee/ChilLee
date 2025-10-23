---
name: "Python 함수형 프로그래밍 가이드"
description: "순수 함수 기반, 불변성 준수, 고차 함수 활용하는 Python 코드 작성. 모든 Python 코드 작성 시 적용"
---

# Python 함수형 프로그래밍 가이드

## 핵심 원칙

이 가이드는 **모든 Python 코드 작성 시** 반드시 적용합니다.

### 1. 불변성 엄격히 준수

**필수 사항:**
- 리스트/딕셔너리 수정 금지 → 새로운 객체 반환
- 변수 재할당 최소화
- `tuple`, `frozenset` 적극 활용
- 데이터 클래스는 `@dataclass(frozen=True)` 사용

**좋은 예:**
```python
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class User:
    name: str
    age: int

def add_user(users: tuple[User, ...], new_user: User) -> tuple[User, ...]:
    """불변 방식으로 사용자 추가"""
    return users + (new_user,)

def update_age(user: User, new_age: int) -> User:
    """새 객체 반환"""
    return User(name=user.name, age=new_age)
```

**나쁜 예 (절대 사용 금지):**
```python
def add_user(users: list, new_user):
    users.append(new_user)  # ❌ 원본 수정
    return users

def update_age(user, new_age):
    user.age = new_age  # ❌ 객체 변경
    return user
```

### 2. 고차 함수 적극 활용

**필수 패턴:**
- `map()`, `filter()`, `reduce()` 우선 사용
- 리스트 컴프리헨션보다 함수형 접근 선호
- `functools`, `itertools` 적극 활용

**좋은 예:**
```python
from functools import reduce
from typing import Callable, Iterable

def compose(*functions: Callable) -> Callable:
    """함수 합성"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def process_users(users: Iterable[User]) -> Iterable[User]:
    """고차 함수로 데이터 처리"""
    return compose(
        lambda us: filter(lambda u: u.age >= 18, us),
        lambda us: map(lambda u: User(u.name.upper(), u.age), us),
    )(users)
```

**나쁜 예:**
```python
def process_users(users):
    result = []
    for user in users:  # ❌ 명령형 루프
        if user.age >= 18:
            result.append(User(user.name.upper(), user.age))
    return result
```

### 3. 사이드 이펙트 최소화

**순수 함수 규칙:**
- 함수 외부 상태 변경 금지
- 함수 인자만으로 결과 결정
- I/O 작업은 명확히 분리
- 예외보다 `Result` 타입 사용 권장

**좋은 예:**
```python
from typing import Union, Callable
from dataclasses import dataclass

@dataclass(frozen=True)
class Success:
    value: any

@dataclass(frozen=True)
class Failure:
    error: str

Result = Union[Success, Failure]

def divide(a: float, b: float) -> Result:
    """순수 함수 - 예외 없이 결과 반환"""
    if b == 0:
        return Failure("Division by zero")
    return Success(a / b)

def map_result(result: Result, func: Callable) -> Result:
    """Result 타입에 함수 적용"""
    match result:
        case Success(value):
            return Success(func(value))
        case Failure(error):
            return Failure(error)
```

**나쁜 예:**
```python
# ❌ 전역 상태 사용
counter = 0

def increment():
    global counter  # ❌ 외부 상태 변경
    counter += 1
    return counter

# ❌ 예외 던지기
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")  # ❌ 사이드 이펙트
    return a / b
```

## 권장 라이브러리
```python
# 함수형 프로그래밍 지원
from functools import reduce, partial, wraps
from itertools import chain, groupby, starmap
from operator import itemgetter, attrgetter

# 타입 힌팅 (필수)
from typing import Callable, Iterable, TypeVar, Protocol
from collections.abc import Sequence
```

## 추가 패턴

### 파이프라인 구성
```python
from functools import reduce
from typing import Callable, TypeVar

T = TypeVar('T')

def pipe(value: T, *functions: Callable) -> any:
    """값을 함수 파이프라인에 통과"""
    return reduce(lambda v, f: f(v), functions, value)

# 사용 예
result = pipe(
    [1, 2, 3, 4, 5],
    lambda xs: filter(lambda x: x % 2 == 0, xs),
    lambda xs: map(lambda x: x ** 2, xs),
    tuple
)  # (4, 16)
```

### 커링(Currying)
```python
from functools import partial

def curry_multiply(x: int) -> Callable[[int], int]:
    """커링된 곱셈 함수"""
    return lambda y: x * y

double = curry_multiply(2)
triple = curry_multiply(3)

# 또는 partial 사용
multiply = lambda x, y: x * y
double = partial(multiply, 2)
```

## 코드 리뷰 체크리스트

코드 작성 후 다음을 반드시 확인:
- [ ] 모든 함수가 순수 함수인가?
- [ ] 원본 데이터를 수정하지 않는가?
- [ ] 변수 재할당이 최소화되었는가?
- [ ] 고차 함수를 활용했는가?
- [ ] 타입 힌트가 명확한가?
- [ ] 사이드 이펙트가 명시적으로 분리되었는가?

## 성능 고려사항

- 대용량 데이터: `itertools` 사용하여 lazy evaluation
- 재귀 깊이 제한: `functools.lru_cache` 또는 꼬리 재귀 최적화 고려
- 필요시 제너레이터 표현식 사용

---

**중요**: 이 가이드는 모든 Python 코드 작성 요청에 자동으로 적용됩니다.