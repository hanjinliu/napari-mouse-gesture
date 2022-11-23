import itertools

import pytest

from napari_mouse_gesture._gesture import GestureCombo

conv = itertools.combinations_with_replacement


def test_from_string():
    GestureCombo.from_string("up")
    GestureCombo.from_string("down")
    GestureCombo.from_string("up-left")
    GestureCombo.from_string("left-right")
    with pytest.raises(ValueError):
        GestureCombo.from_string("up-up")


def test_from_arrows():
    GestureCombo.from_arrows("↑")
    GestureCombo.from_arrows("↓")
    GestureCombo.from_arrows("↑←")
    GestureCombo.from_arrows("←→")
    with pytest.raises(ValueError):
        GestureCombo.from_arrows("↑↑")


def test_from_triangles():
    GestureCombo.from_triangles("^")
    GestureCombo.from_triangles("v")
    GestureCombo.from_triangles("^<")
    GestureCombo.from_triangles("<>")
    with pytest.raises(ValueError):
        GestureCombo.from_triangles("^^")


@pytest.mark.parametrize(
    "a, b, c",
    [
        ("up", "^", "↑"),
        ("down", "v", "↓"),
        ("left", "<", "←"),
        ("right", ">", "→"),
        ("up-left", "^<", "↑←"),
        ("left-right", "<>", "←→"),
    ],
)
def test_same_hash(a, b, c):
    g0 = GestureCombo.from_string(a)
    g1 = GestureCombo.from_triangles(b)
    g2 = GestureCombo.from_arrows(c)
    assert hash(g0) == hash(g1) == hash(g2)


def test_same_hash_in_dict():
    d = {}
    g0 = GestureCombo.from_string("up")
    g1 = GestureCombo.from_string("up")
    d[g0] = 0
    assert g1 in d
    d[g1]


def test_no_collision():
    gestures = [
        "^",
        "v",
        "<",
        ">",
        "<^",
        "v>",
        "^<",
        ">v",
        "^v^",
        ">^<",
        "^<^",
        "^<v",
        "^v<",
        "<><",
    ]

    all_hashes = list(hash(GestureCombo.from_triangles(x)) for x in gestures)
    assert len(all_hashes) == len(set(all_hashes))
