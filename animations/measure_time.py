from movement_types import BP
from animation import Animation, AnimationFrame
from position import Position

# The values are added to the starting position
# Values are in  percentage of movement range (offset - max_value)
measure_time = Animation(
    [
        AnimationFrame(Position(
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
            }),
        ),
        AnimationFrame(
            Position(
            {
                BP.nose: 0,
                BP.head: 0,
                BP.body: 0,
                BP.tail: 0,
                BP.l_wingtip: 50,
                BP.l_wingmid: 50,
                BP.l_winginner: 0,
                BP.r_winginner: 0,
                BP.r_wingmid: 50,
                BP.r_wingtip: 50,
            }),
            delays={
                BP.l_wingtip: 0,
                BP.l_wingmid: 2,
                BP.r_wingmid: 2,
                BP.r_wingtip: 0,
            }
        ),
        AnimationFrame(
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
            }),
            delays={
                BP.l_wingtip: 0,
                BP.l_wingmid: 2,
                BP.r_wingmid: 2,
                BP.r_wingtip: 0,
            }
        ),
        AnimationFrame(
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
            }  ),
        ),
    ],
)
