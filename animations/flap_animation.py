from movement_types import BP
from position import Position
from animation import Animation

from animations.positions import wings_up, wings_down, start_fly, end_fly

# The values are added to the starting position
# Values are in  percentage of movement range (offset - max_value)
flap_animation = Animation(
    [
        start_fly,
        wings_up,
        wings_down,
        end_fly,
    ],
    delays=[3.5,3.5,5],
)
