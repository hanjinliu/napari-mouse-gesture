from typing import TYPE_CHECKING

from qtpy import QtWidgets as QtW

if TYPE_CHECKING:
    import napari


class QMouseGestureWidget(QtW.QWidget):
    def __init__(self, viewer: "napari.Viewer"):
        super().__init__()
        self.viewer = viewer
        self._setup_ui()

    def _setup_ui(self):
        _layout = QtW.QHBoxLayout()
        self.setLayout(_layout)
