import pytest

attempts = {"count": 0}


def test_passes_on_second_try():
    attempts["count"] += 1
    assert attempts["count"] >= 2, f"Попытка {attempts['count']}"