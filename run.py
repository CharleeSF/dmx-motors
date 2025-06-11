import logging
import sys

sys.path.append(".")

from movement_types import Position, BP, Motor, DMX
from mover import mover

from flap_animation import flap_animation

# PLAY SETTINGS
base_offset = 20
max_value = 90
start_position = "neutral"
animation_to_play = "flap"

########################################################################
########################################################################

logging.basicConfig(level=logging.INFO)

dmx = DMX(max_pos_value=max_value)

calibrate = Position(
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

absolute_positions = {
    "neutral": Position(
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
        calibrate=calibrate,
    ),
    "dive": Position(
        {
            BP.nose: 69,
            BP.head: 45,
            BP.body: 20,
            BP.tail: 0,
            BP.l_wingtip: 0,
            BP.l_wingmid: 0,
            BP.l_winginner: 0,
            BP.r_winginner: 0,
            BP.r_wingmid: 0,
            BP.r_wingtip: 0,
        },
        absolute=True,
        calibrate=calibrate,
    ),
}

animations = {
    "flap": flap_animation,
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
    BP.nose: Motor(1),
    BP.head: Motor(11),
    BP.body: Motor(21),
    BP.tail: Motor(31),
    BP.l_wingtip: Motor(41),
    BP.l_wingmid: Motor(51),
    BP.l_winginner: Motor(61),
    BP.r_winginner: Motor(71),
    BP.r_wingmid: Motor(81),
    BP.r_wingtip: Motor(91),
}

import argparse

parser = argparse.ArgumentParser(description="Controller for dmx motors")
parser.add_argument(
    "--live_move", action="store_true", help="Control motors with keyboard"
)
parser.add_argument(
    "--animation_frames",
    action="store_true",
    help="Step through animiation frames with arrow keys",
)
cli_args = parser.parse_args()
# animations[animation_to_play].play(motors, dmx)

# absolute_positions[start_position].setMotors(motors)
# dmx.sendPositions(motors)

if cli_args.live_move:
    mover(motors, dmx)
elif cli_args.animation_frames:
    animations[animation_to_play].stepThrough(motors, dmx, starting_position=absolute_positions[start_position])
