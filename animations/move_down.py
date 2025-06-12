from animation import Animation, AnimationFrame
from movement_types import BP
from position import Position


move_down = Animation(
    [
        AnimationFrame(
            {
                BP.nose: 100,
                BP.head: 57,
                BP.body: 60,
                BP.tail: 0,
                BP.l_wingtip: 5,
                BP.l_wingmid: 13,
                BP.l_winginner: 0,
                BP.r_winginner: 0,
                BP.r_wingmid: 13,
                BP.r_wingtip: 5,
            },
        ),
        AnimationFrame(
            {
                BP.nose: 97,
                BP.head: 71,
                BP.body: 75,
                BP.tail: 23,
                BP.l_wingtip: 5,
                BP.l_wingmid: 13,
                BP.l_winginner: 0,
                BP.r_winginner: 0,
                BP.r_wingmid: 13,
                BP.r_wingtip: 6,
            },
        ),
    ],
)