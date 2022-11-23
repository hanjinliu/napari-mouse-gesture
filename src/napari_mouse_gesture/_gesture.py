from __future__ import annotations

import re
from enum import Enum
from typing import Callable, Iterator, MutableMapping, Sequence, Union


class Patterns:
    """Regular expressions patterns."""

    strings = re.compile(r"^(up|down|left|right)(-(up|down|left|right))*$")
    arrows = re.compile(r"^(↑|←|↓|→)+$")
    triangles = re.compile(r"^(\^|<|v|>)+$")


class Gesture(Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"

    def __repr__(self) -> str:
        s = _ARROWS[self]
        return f"Gesture({s})"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "a":
            return _ARROWS[self]
        elif format_spec == "t":
            return _TRIANGLES[self]
        elif format_spec == "s":
            return self.name
        raise ValueError(f"Unknown format specifier: {format_spec!r}")


# Mapping from Gesture to arrow string, and its inverse mapping.
_ARROWS = {
    Gesture.up: "↑",
    Gesture.down: "↓",
    Gesture.left: "←",
    Gesture.right: "→",
}

_ARROW_TO_GESTURE = {
    "↑": Gesture.up,
    "↓": Gesture.down,
    "←": Gesture.left,
    "→": Gesture.right,
}

# Mapping from Gesture to triangle string, and its inverse mapping.
_TRIANGLES = {
    Gesture.up: "^",
    Gesture.down: "v",
    Gesture.left: "<",
    Gesture.right: ">",
}

_TRIANGLES_TO_GESTURE = {
    "^": Gesture.up,
    "v": Gesture.down,
    "<": Gesture.left,
    ">": Gesture.right,
}

# Mapping from Gesture to its hash.
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
        """Construct a GestureCombo from a string."""
        return cls.from_list(s.split("-"))

    @classmethod
    def from_triangles(cls, s: Sequence[str]) -> GestureCombo:
        """Construct a GestureCombo from a string of triangles."""
        return cls.from_list(_TRIANGLES_TO_GESTURE[c] for c in s)

    @classmethod
    def from_arrows(cls, s: Sequence[str]) -> GestureCombo:
        """Construct a GestureCombo from a string of arrows."""
        return cls.from_list(_ARROW_TO_GESTURE[c] for c in s)

    @classmethod
    def from_list(cls, vals: list[Gesture | str]) -> GestureCombo:
        """Construct a GestureCombo from a list of Gesture or str."""
        last_ges = None
        gestures: list[Gesture] = []
        for v in vals:
            ges = Gesture(v)
            if ges is last_ges:
                raise ValueError(
                    f"Same gesture {ges!r} must not be next to each other."
                )
            gestures.append(ges)
            last_ges = ges
        return cls(gestures)

    @classmethod
    def from_hash(cls, h: int) -> GestureCombo:
        """Construct a GestureCombo from a hash integer."""
        gestures = []
        while h > 0:
            ges = Gesture(h % 16)
            gestures.append(ges)
            h //= 16
        return cls(gestures)

    @classmethod
    def from_any(self, val) -> GestureCombo:
        """Dispatch to the appropriate constructor."""
        if isinstance(val, GestureCombo):
            self = val
        elif isinstance(val, str):
            if Patterns.arrows.match(val):
                return self.from_arrows(val)
            elif Patterns.triangles.match(val):
                return self.from_triangles(val)
            elif Patterns.strings.match(val):
                return self.from_string(val)
            else:
                raise ValueError(f"Invalid gesture string: {val!r}")
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

    def __eq__(self, other: GestureCombo) -> bool:
        if isinstance(other, GestureCombo):
            return hash(self) == hash(other)
        return False

    def __repr__(self) -> str:
        fmt = "".join(format(ges, "a") for ges in self)
        return f"GestureCombo({fmt})"

    def __format__(self, format_spec: str) -> str:
        if format_spec == "s":
            return "-".join(format(ges, format_spec) for ges in self)
        return "".join(format(ges, format_spec) for ges in self)


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

    def __contains__(self, other) -> bool:
        try:
            self._registry[other]
        except Exception:
            return False
        return True

    def __iter__(self):
        return iter(self._registry)

    def __len__(self):
        return len(self._registry)

    def __repr__(self) -> str:
        strs: list[str] = []
        for ges, func in self._registry.items():
            strs.append(f"{ges!r}: {func!r}")
        s = ",\n\t".join(strs)
        return f"GestureRegistry(\n\t{s}\n)"


GestureLike = Union[str, Sequence[str], GestureCombo]
