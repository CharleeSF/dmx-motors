from movement_types import BP
from animation import Animation
from position import Position

from animations.positions import wings_up, wings_down, start_fly, end_fly

# The values are added to the starting position
# Values are in  percentage of movement range (offset - max_value)
measure_time = Animation(
    [
        Position(
            {
                BP.nose: 0,
                BP.head: 0,
                BP.body: 0,
                BP.tail: 0,
                BP.l_wingtip: 0,
                BP.l_wingmid: 0,
                BP.l_winginner: 0,
                BP.r_winginner: 0,
                BP.r_wingmid: 0,
                BP.r_wingtip: 0,
            },
        ),
        Position(
            {
                BP.nose: 0,
                BP.head: 0,
                BP.body: 0,
                BP.tail: 0,
                BP.l_wingtip: 100,
                BP.l_wingmid: 50,
                BP.l_winginner: 0,
                BP.r_winginner: 0,
                BP.r_wingmid: 50,
                BP.r_wingtip: 100,
            },
        ),
        Position(
            {
                BP.nose: 0,
                BP.head: 0,
                BP.body: 0,
                BP.tail: 0,
                BP.l_wingtip: 0,
                BP.l_wingmid: 0,
                BP.l_winginner: 0,
                BP.r_winginner: 0,
                BP.r_wingmid: 0,
                BP.r_wingtip: 0,
            },
        ),
        Position(
            {
                BP.nose: 0,
                BP.head: 0,
                BP.body: 0,
                BP.tail: 0,
                BP.l_wingtip: 0,
                BP.l_wingmid: 0,
                BP.l_winginner: 0,
                BP.r_winginner: 0,
                BP.r_wingmid: 0,
                BP.r_wingtip: 0,
            },
        ),
    ],

    # delays=[6]*4,
)
