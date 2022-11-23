from __future__ import annotations

import numpy as np

from napari_mouse_gesture._gesture import Gesture, GestureCombo

# Classifiers that classifies a (N, 2) trajectory into gestures.

_RES_TO_GESTURE = {
    0: Gesture.right,
    1: Gesture.down,
    2: Gesture.left,
    3: Gesture.up,
}


def diff_classifier(traj: np.ndarray):
    if traj.shape[0] < 2:
        return GestureCombo([])
    # remove small movements
    dtraj = np.diff(traj, axis=0)
    each_length = np.sqrt(np.sum(dtraj**2, axis=1))
    length = np.sum(each_length)

    is_small = each_length < length / 100
    is_small = np.concatenate([[False], is_small], axis=0)

    traj = traj[~is_small]

    # calculate angles
    if traj.shape[0] < 2:
        return GestureCombo([])
    dtraj = np.diff(traj, axis=0)
    angle = np.arctan2(dtraj[:, 0], dtraj[:, 1])
    pi2 = np.pi / 2
    res = ((angle + pi2 / 2) // pi2) % 4

    gestures = []
    last_r = None
    for r in res:
        if last_r != r:
            gestures.append(_RES_TO_GESTURE[r])
            last_r = r

    return GestureCombo(gestures)
