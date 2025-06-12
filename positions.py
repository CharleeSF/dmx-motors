from movement_types import BP
from position import Position

# Values are in percentage of movement range (offset - max_value)

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
        BP.nose: 100,
        BP.head: 55,
        BP.body: 0,
        BP.tail: 24,
        BP.l_wingtip: 100,
        BP.l_wingmid: 40,
        BP.l_winginner: 0,
        BP.r_winginner: 0,
        BP.r_wingmid: 40,
        BP.r_wingtip: 100,
    },
)

lean_right = Position(
    {
        BP.nose: 50,
        BP.head: 50,
        BP.body: 44,
        BP.tail: 44,
        BP.l_wingtip: 0,
        BP.l_wingmid: 0,
        BP.l_winginner: 0,
        BP.r_winginner: 53,
        BP.r_wingmid: 89,
        BP.r_wingtip: 100,
    },
    absolute=True,
)

lean_left = Position(
    {
        BP.nose: 50,
        BP.head: 50,
        BP.body: 44,
        BP.tail: 44,
        BP.l_wingtip: 100,
        BP.l_wingmid: 89,
        BP.l_winginner: 53,
        BP.r_winginner: 0,
        BP.r_wingmid: 0,
        BP.r_wingtip: 0,
    },
    absolute=True,
)

zero = Position(
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
    absolute=True,
)

mid = Position(
    {
        BP.nose: 50,
        BP.head: 50,
        BP.body: 50,
        BP.tail: 50,
        BP.l_wingtip: 50,
        BP.l_wingmid: 50,
        BP.l_winginner: 50,
        BP.r_winginner: 50,
        BP.r_wingmid: 50,
        BP.r_wingtip: 50,
    },
    absolute=True,
)

dive = Position(
    {
        BP.nose: 100,
        BP.head: 80,
        BP.body: 40,
        BP.tail: 0,
        BP.l_wingtip: 0,
        BP.l_wingmid: 0,
        BP.l_winginner: 0,
        BP.r_winginner: 0,
        BP.r_wingmid: 0,
        BP.r_wingtip: 0,
    },
    absolute=True,
)