from movement_types import Position, BP
from animation import Animation

# The values are added to the starting position
# Values are in  percentage of movement range (offset - max_value)
flap_animation = Animation(
    [
        Position(
            {
                BP.nose: 100,
                BP.head: 90,
                BP.body: 80,
                BP.tail: 80,
                BP.l_wingtip: 0,
                BP.l_wingmid: 25,
                BP.l_winginner: 10,
                BP.r_winginner: 10,
                BP.r_wingmid: 25,
                BP.r_wingtip: 0,
            },
        ),
        Position(
            {
                BP.nose: 80,
                BP.head: 70,
                BP.body: 30,
                BP.tail: 20,
                BP.l_wingtip: 100,
                BP.l_wingmid: 40,
                BP.l_winginner: 0,
                BP.r_winginner: 0,
                BP.r_wingmid: 40,
                BP.r_wingtip: 100,
            },
        ),
    ]
)
