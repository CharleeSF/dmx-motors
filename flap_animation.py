from movement_types import Position, BP
from animation import Animation

flap_animation = Animation(
    [
        Position(
            {
                BP.nose: 39,
                BP.head: 32,
                BP.body: 39,
                BP.tail: 39,
                BP.l_wingtip: 0,
                BP.l_wingmid: 10,
                BP.l_winginner: 9,
                BP.r_winginner: 9,
                BP.r_wingmid: 10,
                BP.r_wingtip: 0,
            },
            absolute=False,
        ),
        Position(
            {
                BP.nose: -4,
                BP.head: 0,
                BP.body: -15,
                BP.tail: -20,
                BP.l_wingtip: 51,
                BP.l_wingmid: 20,
                BP.l_winginner: -2,
                BP.r_winginner: -3,
                BP.r_wingmid: 20,
                BP.r_wingtip: 51,
            },
            absolute=False,
        ),
    ]
)
