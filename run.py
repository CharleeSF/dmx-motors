import sys

sys.path.append(".")

from movement_types import Position, Animation, BP, Motor, DMX

# PLAY SETTINGS
base_offset = 0
start_position = "zero"
animation_to_play = "flap"

########################################################################
########################################################################

dmx = DMX()

absolute_positions = {
    "zero": Position(
        {
            BP.nose: 60,
            BP.head: 50,
            BP.body: 70,
            BP.tail: 60,
            BP.ltw: 55,
            BP.lmw: 15,
            BP.liw: 60,
            BP.riw: 60,
            BP.rmw: 35,
            BP.rtw: 55,
        },
        absolute=True,
    )
}

animations = {
    "flap": Animation(
        [
            Position(
                {
                    BP.nose: 0,
                    BP.head: 0,
                    BP.body: 0,
                    BP.tail: 0,
                    BP.ltw: 0,
                    BP.lmw: 0,
                    BP.liw: 0,
                    BP.rtw: 0,
                    BP.rmw: 0,
                    BP.riw: 0,
                },
                absolute=False,
                delay=5,
            ),
        ]
    ),
}


# 1: nose
# 11: head
# 21: body
# 31: tail
# 41: left wing tip
# 51: left middle wing
# 61: left inner wing
# 71: right wing tip
# 81: right middle wing
# 91: right inner wing
motors = {
    BP.nose: Motor(1, base_offset),
    BP.head: Motor(11, base_offset),
    BP.body: Motor(21, base_offset),
    BP.tail: Motor(31, base_offset),
    BP.ltw: Motor(41, base_offset),
    BP.lmw: Motor(51, base_offset),
    BP.liw: Motor(61, base_offset),
    BP.riw: Motor(71, base_offset),
    BP.rmw: Motor(81, base_offset),
    BP.rtw: Motor(91, base_offset),
}

absolute_positions[start_position].setMotors(motors)
dmx.sendPositions(motors)
# animations[animation_to_play].play(motors, dmx)
