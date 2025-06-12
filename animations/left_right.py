from animation import Animation, AnimationFrame
from movement_types import BP
from position import Position

import positions

left_right = Animation(
    loop_frames = [
        AnimationFrame(
            positions.lean_right, hold=6
        ),
        AnimationFrame(
            positions.lean_left, hold=6
        ),
    ],
)