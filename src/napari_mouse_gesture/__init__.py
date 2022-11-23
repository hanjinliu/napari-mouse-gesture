__version__ = "0.0.1"

from ._main import current_instance, register_gesture
from ._widget import QMouseGestureWidget

__all__ = ["QMouseGestureWidget", "current_instance", "register_gesture"]
