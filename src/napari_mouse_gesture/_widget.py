from typing import TYPE_CHECKING

from qtpy import QtWidgets as QtW

if TYPE_CHECKING:
    import napari

    from napari_mouse_gesture._gesture import GestureCombo


class QMouseGestureWidget(QtW.QWidget):
    def __init__(self, viewer: "napari.Viewer"):
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
        _layout.addWidget(self._gesture_line_edit)

        self._activate_viewer_gesture_box = QtW.QCheckBox(
            "Activate viewer gesture"
        )
        self._activate_viewer_gesture_box.toggled.connect(
            self._on_viewer_activation_changed
        )
        _layout.addWidget(self._activate_viewer_gesture_box)

    def _on_gestured(self, ges: "GestureCombo"):
        self._gesture_line_edit.setText(f"{ges:a}")

    def _on_viewer_activation_changed(self, checked: bool):
        if checked:
            self._gesture_provider.set_viewer_gesture()
        else:
            self._gesture_provider.reset_viewer_gesture()
