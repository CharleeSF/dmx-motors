from movement_types import BP
from position import Position

start_fly = Position(
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
)

end_fly = Position(
    {
        BP.nose: 100,
        BP.head: 46,
        BP.body: 0,
        BP.tail: 0,
        BP.l_wingtip: 0,
        BP.l_wingmid: 38,
        BP.l_winginner: 0,
        BP.r_winginner: 0,
        BP.r_wingmid: 38,
        BP.r_wingtip: 0,
    },
)


wings_up = Position(
    {
        BP.nose: 100,
        BP.head: 60,
        BP.body: 100,
        BP.tail: 100,
        BP.l_wingtip: 0,
        BP.l_wingmid: 30,
        BP.l_winginner: 70,
        BP.r_winginner: 70,
        BP.r_wingmid: 30,
        BP.r_wingtip: 0,
    },
)

wings_down = Position(
    {
        BP.nose: 80,
        BP.head: 40,
        BP.body: 0,
        BP.tail: 0,
        BP.l_wingtip: 100,
        BP.l_wingmid: 40,
        BP.l_winginner: 0,
        BP.r_winginner: 0,
        BP.r_wingmid: 40,
        BP.r_wingtip: 100,
    },
)