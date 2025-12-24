# test_quality_single.py
"""
단일 파일 버전: 함수 정의 + pytest 테스트
이 파일 하나로 테스트/커버리지/린트 입력용 샘플을 구성합니다.

실행 예:
  pip install pytest pytest-cov coverage ruff
  pytest -q --maxfail=1 --junitxml=pytest.xml --cov=. --cov-report=xml:coverage.xml
  # 또는
  coverage run -m pytest -q --maxfail=1 --junitxml=pytest.xml && coverage xml
  ruff check . --output-format json > ruff.json || true
"""

# -------------------------
# 기능 코드 (입력으로 사용할 부분)
# -------------------------

from __future__ import annotations
from typing import Iterable, Sequence
import re


def weighted_sum(values: Iterable[tuple[float, float]]) -> float:
    """
    가중합을 계산한다.
    values: (value, weight) 튜플들의 이터러블
    """
    total = 0.0
    for v, w in values:
        total += float(v) * float(w)
    return total


def moving_average(seq: Sequence[float], window: int) -> list[float]:
    """
    단순 이동평균. window는 1 이상이어야 한다.
    길이가 n인 시퀀스에 대해 길이 n - window + 1의 결과를 반환한다.
    """
    if window <= 0:
        raise ValueError("window must be >= 1")
    n = len(seq)
    if window > n:
        return []
    out: list[float] = []
    s = sum(seq[:window])
    out.append(s / window)
    for i in range(window, n):
        # 다음 윈도우 = 이전 합 + 새로 들어온 값 - 윈도우에서 빠지는 값
        s += seq[i] - seq[i - window]
        out.append(s / window)
    return out


def revenue(items: Iterable[dict]) -> float:
    """
    매출 합계를 계산한다.
    각 항목은 {'qty': 수량, 'unit_price': 단가} 키를 가진다. 결측은 0으로 처리한다.
    """
    total = 0.0
    for it in items:
        q = float(it.get("qty", 0) or 0)
        p = float(it.get("unit_price", 0) or 0)
        total += q * p
    return total


def grade(total: float) -> str:
    """
    점수에 따른 등급을 반환한다.
    """
    if total >= 90:
        return "A"
    if total >= 80:
        return "B"
    if total >= 70:
        return "C"
    if total >= 60:
        return "D"
    return "F"


_space_re = re.compile(r"\s+")


def normalize_whitespace(s: str) -> str:
    """
    공백을 하나로 축약하고 앞뒤 공백을 제거한다.
    """
    if s is None:
        raise ValueError("s must not be None")
    return _space_re.sub(" ", s).strip()


def is_palindrome(s: str) -> bool:
    """
    영숫자만 남기고 소문자로 변환한 뒤 회문 여부를 확인한다.
    """
    if s is None:
        return False
    cleaned = re.sub(r"[^0-9a-zA-Z]", "", s).lower()
    return cleaned == cleaned[::-1]


def summarize(text: str, max_len: int = 80) -> str:
    """
    길이가 max_len을 넘으면 말줄임표를 붙여 잘라낸다.
    """
    if max_len < 4:
        raise ValueError("max_len must be >= 4")
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def mask_email(email: str) -> str:
    """
    이메일 로컬파트를 마스킹한다. abcd@example.com -> a**d@example.com
    형식이 아니면 그대로 반환한다.
    """
    if "@" not in email:
        return email
    local, domain = email.split("@", 1)
    if len(local) <= 1:
        masked = "*"
    elif len(local) == 2:
        masked = local[0] + "*"
    else:
        masked = local[0] + "*" * (len(local) - 2) + local[-1]
    return masked + "@" + domain


# -------------------------
# 테스트 코드 (pytest가 이 파일에서 바로 수집)
# -------------------------

def test_weighted_sum_basic():
    assert weighted_sum([(10, 0.5), (20, 0.5)]) == 15.0
    assert weighted_sum([]) == 0.0


def test_moving_average_basic():
    assert moving_average([1, 2, 3, 4], 2) == [1.5, 2.5, 3.5]


def test_moving_average_window_edge():
    assert moving_average([1, 2, 3], 1) == [1.0, 2.0, 3.0]
    assert moving_average([1, 2, 3], 5) == []


def test_moving_average_invalid():
    import pytest
    with pytest.raises(ValueError):
        moving_average([1, 2, 3], 0)


def test_revenue_and_grade():
    items = [
        {"qty": 2, "unit_price": 5000},
        {"qty": 1, "unit_price": 12000},
        {"qty": None, "unit_price": 9999},
    ]
    assert revenue(items) == 22000.0
    assert grade(95) == "A"
    assert grade(81) == "B"
    assert grade(74) == "C"
    assert grade(60) == "D"
    assert grade(12) == "F"


def test_normalize_whitespace():
    assert normalize_whitespace("  a   b    c ") == "a b c"


def test_is_palindrome():
    assert is_palindrome("Never odd or even")
    assert not is_palindrome("hello")


def test_summarize_and_email():
    s = "x" * 100
    assert summarize(s, max_len=10) == "xxxxxxx..."
    assert summarize("short", max_len=10) == "short"
    masked = mask_email("abcd@example.com")
    assert masked.startswith("a")
    assert "@example.com" in masked
