from __future__ import annotations

import weakref
from contextlib import contextmanager
from typing import TYPE_CHECKING, Callable, TypeVar

import numpy as np
from psygnal import Signal

from napari_mouse_gesture._classifier import diff_classifier
from napari_mouse_gesture._gesture import (
    GestureCombo,
    GestureLike,
    GestureRegistry,
)
from napari_mouse_gesture._types import LayerInfo, MouseEvent, Trigger

if TYPE_CHECKING:
    import napari
    from napari.layers import Layer

_F = TypeVar("_F", bound=Callable)
MOUSE_MOVE = "mouse_move"


class MouseGestureProvider:
    gestured = Signal(GestureCombo)
    _current_instance: MouseGestureProvider | None = None

    def __init__(
        self,
        viewer: napari.Viewer,
        trigger: Trigger | str = Trigger.rightclick,
    ):
        self._trigger = Trigger(trigger)
        self._viewer_ref = weakref.ref(viewer)
        self._registry = GestureRegistry()

        self.gestured.connect(self._call_callbacks)

        self.__class__._current_instance = self

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

    def _call_callbacks(self, combo: GestureCombo):
        if cb := self._registry.get(combo):
            cb(self.viewer)

    def set_viewer_gesture(self):
        self.viewer.mouse_drag_callbacks.append(self.viewer_mouse_callback)
        return None

    def reset_viewer_gesture(self):
        self.viewer.mouse_drag_callbacks.remove(self.viewer_mouse_callback)
        return None

    def set_layer_gesture(self, layer: Layer):
        layer.mouse_drag_callbacks.append(self.layer_mouse_callback)
        return None

    def reset_layer_gesture(self, layer: Layer):
        layer.mouse_drag_callbacks.remove(self.layer_mouse_callback)
        return None

    @contextmanager
    def dragging(self):
        """Temporary context for mouse gesture."""
        # get selected layers first
        layers = list(self.viewer.layers.selection)

        # disable selected layers
        layer_infos: list[LayerInfo] = []
        for layer in layers:
            layer_infos.append(LayerInfo.from_layer(layer))
            layer.interactive = False

        try:
            yield
        finally:
            # restore original state
            for layer, interactive in layer_infos:
                if layer not in self.viewer.layers:
                    layers.remove(layer)
                layer.interactive = interactive
            self.viewer.layers.selection = layers

    def viewer_mouse_callback(self, viewer: napari.Viewer, event: MouseEvent):
        """Callback function for viewer mouse drag event."""
        if event.button != 2:
            return

        with self.dragging():
            points = np.asarray(event.position).reshape(1, 2)
            yield
            while event.type == MOUSE_MOVE:
                points = np.append(
                    points, np.asarray(event.position).reshape(1, 2), axis=0
                )
                yield
        self._call_by_trajectory(points)

        return None

    def layer_mouse_callback(self, layer: Layer, event: MouseEvent):
        """Callback function for layer mouse drag event."""
        if event.button != 2:
            return

        with self.dragging():
            points = np.asarray(event.position).reshape(1, 2)
            yield
            while event.type == MOUSE_MOVE:
                np.append(
                    points, np.asarray(event.position).reshape(1, 2), axis=0
                )
                yield

        self._call_by_trajectory(points)
        return None

    def _call_by_trajectory(self, traj: np.ndarray):
        combo = diff_classifier(traj)
        self.gestured.emit(combo)
        return None

    def register_gesture(
        self,
        gesture: GestureLike,
        *,
        overwrite: bool = False,
    ) -> Callable[[_F], _F]:
        """
        Register a callback function for the given gesture.

        You can use arrows (???, ???, ???, ???)
        >>> @provider.register_gesture("??????")
        >>> def do_something(viewer):
        >>>     ...

        or triangles (^, <, v, >)
        >>> @provider.register_gesture("^<")
        >>> def do_something(viewer):
        >>>     ...

        or words (up, down, left, right) split by "-".
        >>> @provider.register_gesture("up-left")
        >>> def do_something(viewer):
        >>>     ...

        Parameters
        ----------
        gesture : GestureLike
            Gesture string.
        overwrite : bool, default is False
            If true, allow to overwrite the existing gesture.
        """

        def wrapper(func):
            if not overwrite and gesture in self._registry:
                raise ValueError(
                    f"Gesture {gesture} already exists. Use `overwrite=True`"
                    " to overwrite it."
                )
            self._registry[gesture] = func
            return func

        return wrapper


def current_instance() -> MouseGestureProvider | None:
    """Return the current instance of MouseGestureProvider."""
    return MouseGestureProvider._current_instance


def register_gesture(
    gesture: GestureLike,
    *,
    overwrite: bool = False,
) -> Callable[[_F], _F]:
    ins = MouseGestureProvider._current_instance
    if ins is None:
        raise RuntimeError("No instance of MouseGestureProvider is found.")
    return ins.register_gesture(gesture, overwrite=overwrite)


register_gesture.__doc__ = MouseGestureProvider.register_gesture.__doc__
