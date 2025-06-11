import logging
import sys

sys.path.append(".")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S"
)

from movement_types import Position, BP, Motor, DMX
from mover import mover
from animation import Animation
from playbook import Playbook, PlaybookItem

from animations import flap_animation
from animations import move_down

# PLAY SETTINGS
min_pos_dmx = 0
max_pos_dmx = 50
min_speed_dmx = 200 # 255 Is the slowest possible
max_speed_dmx = 50 # 0 Is the fastest possible
start_position = "zero"
animation_to_play = "flap"

########################################################################
########################################################################

logging.basicConfig(level=logging.INFO)

dmx = DMX(min_pos_dmx=min_pos_dmx, max_pos_dmx=max_pos_dmx, min_speed_dmx=min_speed_dmx, max_speed_dmx=max_speed_dmx)

# The values are added to 0
# Values are in  percentage of movement range (offset - max_value)
starting_positions = {
    "zero": Position(
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
    ),
    "mid": Position(
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
    ),
    "dive": Position(
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
    ),
}

animations = {
    "flap": flap_animation,
    "move_down": move_down,
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
parser.add_argument(
    "--play",
    action="store_true",
    help="Play animation",
)
cli_args = parser.parse_args()
# animations[animation_to_play].play(motors, dmx)

# starting_positions[start_position].setMotors(motors)
# dmx.sendPositions(motors)

playbook = Playbook(
    playbook=[
        PlaybookItem(item=starting_positions["zero"], time_s=6, text="Go to zero"),
        PlaybookItem(item=animations["flap"], loops=4, scale=1, text="High flap (2x)"),
        # PlaybookItem(item=starting_positions["zero"], time_s=5, text="Return to zero"),
        # PlaybookItem(item=animations["move_down"], loops=1, scale=1, text="Move down (full)"),
        # PlaybookItem(item=starting_positions["mid"], time_s=5, text="Go to mid"),
        # PlaybookItem(item=animations["flap"], loops=1, scale=0.7, text="Mid flap (2x)"),
    ]
)

if cli_args.live_move:
    mover(motors, dmx)
elif cli_args.animation_frames:
    animations[animation_to_play].stepThrough(motors, dmx, starting_position=starting_positions[start_position])
elif cli_args.play:
    animations[animation_to_play].play(motors, dmx, starting_position=starting_positions[start_position])
else:
    playbook.play(motors, dmx)
