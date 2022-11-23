from typing import TYPE_CHECKING

import napari
from qtpy import QtCore
from qtpy import QtWidgets as QtW

if TYPE_CHECKING:
    from napari_mouse_gesture._gesture import GestureCombo


class QMouseGestureWidget(QtW.QWidget):
    def __init__(self, viewer: napari.Viewer):
        from napari_mouse_gesture._main import MouseGestureProvider

        super().__init__()
        self._gesture_provider = MouseGestureProvider(viewer)
        self.viewer = viewer
        self._setup_ui()

        self._gesture_provider.gestured.connect(self._on_gestured)

    def _setup_ui(self):
        _layout = QtW.QVBoxLayout()
        self.setLayout(_layout)

        self._gesture_line_edit = QtW.QLineEdit()
        self._gesture_line_edit.setReadOnly(True)
        font = self._gesture_line_edit.font()
        font.setPointSize(22)
        self._gesture_line_edit.setFont(font)
        _layout.addWidget(self._gesture_line_edit)

        self._activate_viewer_gesture_box = QtW.QCheckBox(
            "Activate viewer gesture"
        )
        self._activate_viewer_gesture_box.toggled.connect(
            self._on_viewer_activation_changed
        )
        _layout.addWidget(self._activate_viewer_gesture_box)

    def _on_gestured(self, ges: "GestureCombo"):
        # update line edit
        text = f"{ges:a}"
        self._gesture_line_edit.setText(text)

        # clear it later
        def _clear():
            if self._gesture_line_edit.text() == text:
                self._gesture_line_edit.setText("")

        QtCore.QTimer.singleShot(1600, _clear)

    def _on_viewer_activation_changed(self, checked: bool):
        if checked:
            self._gesture_provider.set_viewer_gesture()
        else:
            self._gesture_provider.reset_viewer_gesture()
