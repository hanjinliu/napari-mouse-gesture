from __future__ import annotations

import weakref
from contextlib import contextmanager
from typing import TYPE_CHECKING

import numpy as np

from napari_mouse_gesture._classifier import diff_classifier
from napari_mouse_gesture._gesture import GestureRegistry
from napari_mouse_gesture._types import LayerInfo, MouseEvent, Trigger

if TYPE_CHECKING:
    import napari
    from napari.layers import Layer

MOUSE_MOVE = "mouse_move"


class MouseGestureProvider:
    def __init__(
        self,
        viewer: napari.Viewer,
        trigger: Trigger | str = Trigger.rightclick,
    ):
        self._trigger = Trigger(trigger)
        self._viewer_ref = weakref.ref(viewer)
        self._registry = GestureRegistry()

    @property
    def trigger(self) -> Trigger:
        """The trigger of mouse gesture."""
        return self._trigger

    @property
    def viewer(self) -> napari.Viewer:
        """The viewer of the provider."""
        viewer = self._viewer_ref()
        if viewer is None:
            raise RuntimeError("The viewer has been garbage collected.")
        return viewer

    def set_viewer_gesture(self):
        self.viewer.mouse_drag_callbacks.append(self.viewer_mouse_callback)
        return None

    def set_layer_gesture(self, layer: Layer):
        layer.mouse_drag_callbacks.append(self.layer_mouse_callback)
        return None

    @contextmanager
    def temporary_layer(self):
        """Create a temporary layer for displaying mouse gesture."""
        layers = list(
            self.viewer.layers.selection
        )  # get selected layers first

        # prepare temporary layer
        temp_layer = self.viewer.add_shapes(
            [[[0, 0], [0, 0]]],
            edge_color=[(0, 1, 0, 0.4)],
            edge_width=10,
            shape_type="path",
            name="Temporary Layer",
        )

        # disable selected layers
        layer_infos: list[LayerInfo] = []
        for layer in layers:
            layer_infos.append(LayerInfo.from_layer(layer))
            layer.interactive = False

        try:
            temp_layer.interactive = False
            yield temp_layer
        finally:
            # restore original state
            self.viewer.layers.remove(temp_layer)
            for layer, interactive in layer_infos:
                if layer not in self.viewer.layers:
                    layers.remove(layer)
                layer.interactive = interactive
            self.viewer.layers.selection = layers

    def viewer_mouse_callback(self, viewer: napari.Viewer, event: MouseEvent):
        if event.button != 2:
            return

        with self.temporary_layer() as temp_layer:
            points = np.asarray(event.position).reshape(1, 2)
            yield
            while event.type == MOUSE_MOVE:
                points = np.append(
                    points, np.asarray(event.position).reshape(1, 2), axis=0
                )
                temp_layer.data = points
                yield
        self._call_by_trajectory(points)

        return None

    def layer_mouse_callback(self, layer: Layer, event: MouseEvent):
        if event.button != 2:
            return

        with self.temporary_layer() as temp_layer:
            points = np.asarray(event.position).reshape(1, 2)
            yield
            while event.type == MOUSE_MOVE:
                np.append(
                    points, np.asarray(event.position).reshape(1, 2), axis=0
                )
                temp_layer.data = points
                yield

        self._call_by_trajectory(points)
        return None

    def _call_by_trajectory(self, traj: np.ndarray):
        print(diff_classifier(traj))
