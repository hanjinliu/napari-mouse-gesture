from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, NamedTuple

import numpy as np

if TYPE_CHECKING:
    from napari.layers import Layer


class MouseEvent:
    """Mimics a napari MouseEvent."""

    blocked: bool
    button: int
    buttons: list[int]
    delta: np.ndarray
    modifiers: list[str]
    type: str
    pos: np.ndarray
    position: np.ndarray


class LayerInfo(NamedTuple):
    layer: Layer
    interactive: bool

    @classmethod
    def from_layer(self, layer: Layer) -> LayerInfo:
        """Construct a LayerInfo from a napari layer."""
        return LayerInfo(layer, layer.interactive)


class Trigger(Enum):
    rightclick = "rightclick"
    ctrl = "ctrl"
    shift = "shift"
