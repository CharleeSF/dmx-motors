import logging
import sys

sys.path.append(".")

from movement_types import Position, Animation, BP, Motor, DMX

# PLAY SETTINGS
base_offset = -10
max_value = 60
start_position = "zero"
animation_to_play = "flap"

########################################################################
########################################################################

logging.basicConfig(level=logging.INFO)

dmx = DMX(max_pos_value=max_value)

absolute_positions = {
    "zero": Position(
        {
            BP.nose: 40,
            BP.head: 25,
            BP.body: 50,
            BP.tail: 60,
            BP.l_wingtip: 55,
            BP.l_wingmid: 15,
            BP.l_winginner: 60,
            BP.r_winginner: 60,
            BP.r_wingmid: 35,
            BP.r_wingtip: 55,
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
                    BP.l_wingtip: 0,
                    BP.l_wingmid: 0,
                    BP.l_winginner: 0,
                    BP.r_wingtip: 0,
                    BP.r_wingmid: 0,
                    BP.r_winginner: 0,
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
    BP.l_wingtip: Motor(41, base_offset),
    BP.l_wingmid: Motor(51, base_offset),
    BP.l_winginner: Motor(61, base_offset),
    BP.r_winginner: Motor(71, base_offset),
    BP.r_wingmid: Motor(81, base_offset),
    BP.r_wingtip: Motor(91, base_offset),
}

absolute_positions[start_position].setMotors(motors)
dmx.sendPositions(motors)
# animations[animation_to_play].play(motors, dmx)
