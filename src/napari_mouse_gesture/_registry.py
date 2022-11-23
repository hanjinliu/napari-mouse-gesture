from __future__ import annotations

from enum import Enum
from typing import Callable, Iterator, MutableMapping


class Gesture(Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"

    def __repr__(self) -> str:
        s = _ARROW_STRING[self]
        return f"Gesture({s})"


_ARROW_STRING = {
    Gesture.up: "↑",
    Gesture.down: "↓",
    Gesture.left: "←",
    Gesture.right: "→",
}

_GESTURE_HASH = {
    Gesture.up: 1,
    Gesture.down: 2,
    Gesture.left: 4,
    Gesture.right: 8,
}


class GestureCombo:
    def __init__(self, gestures: list[Gesture]):
        self._gestures = gestures

    @classmethod
    def from_string(cls, s: str) -> GestureCombo:
        return cls.from_list(s.split("-"))

    @classmethod
    def from_list(cls, gestures: list[Gesture | str]) -> GestureCombo:
        last_ges = None
        gestures: list[Gesture] = []
        for g in gestures:
            ges = Gesture(g)
            if ges is last_ges:
                raise ValueError(
                    f"Same gesture {ges!r} must not be next to each other."
                )
            gestures.append(ges)
        return cls(gestures)

    @classmethod
    def from_hash(cls, h: int) -> GestureCombo:
        gestures = []
        while h > 0:
            ges = Gesture(h % 16)
            gestures.append(ges)
            h //= 16
        return cls(gestures)

    @classmethod
    def from_any(self, val) -> GestureCombo:
        if isinstance(val, str):
            self = GestureCombo.from_string(val)
        elif isinstance(val, int):
            self = GestureCombo.from_hash(val)
        else:
            self = GestureCombo.from_list(val)
        return self

    def __iter__(self) -> Iterator[Gesture]:
        return iter(self._gestures)

    def __hash__(self) -> int:
        return sum(
            _GESTURE_HASH[ges] * (16**i) for i, ges in enumerate(self)
        )


class GestureRegistry(MutableMapping[GestureCombo, Callable]):
    def __init__(self):
        self._registry: dict[GestureCombo, Callable] = {}

    def __getitem__(self, key):
        key = GestureCombo.from_any(key)
        return self._registry[key]

    def __setitem__(self, key, value):
        key = GestureCombo.from_any(key)
        self._registry[key] = value

    def __delitem__(self, key) -> None:
        key = GestureCombo.from_any(key)
        del self._registry[key]

    def __iter__(self):
        return iter(self._registry)

    def __len__(self):
        return len(self._registry)
