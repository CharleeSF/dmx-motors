from animation import Animation, AnimationFrame
from movement_types import BP
from position import Position

import positions

left_right = Animation(
    [
        AnimationFrame(
            positions.lean_right
        ),
        AnimationFrame(
            positions.lean_left
        ),
        AnimationFrame(
            positions.lean_right
        ),
        AnimationFrame(
            positions.lean_left
        ),
    ],
)