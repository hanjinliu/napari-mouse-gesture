from __future__ import annotations

from typing import TYPE_CHECKING

from magicgui.widgets import show_file_dialog

if TYPE_CHECKING:
    import napari


def open_from_path(viewer: napari.Viewer):
    if path := show_file_dialog("r", "Open file"):
        viewer.open(path)
    return viewer
