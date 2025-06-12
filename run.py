import atexit
import logging
import sys

sys.path.append(".")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S"
)

from movement_types import BP, Motor
from position import Position
from DMX import DMX
from mover import mover
from animation import Animation
from playbook import Playbook, PlaybookItem

import animations

import positions

# PLAY SETTINGS
min_pos_dmx = 0
max_pos_dmx = 40
min_speed_dmx = 200 # 255 Is the slowest possible
max_speed_dmx = 50 # 0 Is the fastest possible
start_position = "zero"
animation_to_play = "left_right"

########################################################################
########################################################################

logging.basicConfig(level=logging.INFO)

dmx = DMX(min_pos_dmx=min_pos_dmx, max_pos_dmx=max_pos_dmx, min_speed_dmx=min_speed_dmx, max_speed_dmx=max_speed_dmx)

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

slow_speeds = { bp: 20 for bp in motors.keys() }

playbook = Playbook(
    playbook=[
        PlaybookItem(item=positions.zero, time_s=3, text="Go to zero"),
        PlaybookItem(item=animations.flap_animation, loops=2, scale=.7, text="High flap (2x)"),
        # PlaybookItem(item=positions.zero, time_s=5, text="Return to zero"),
        PlaybookItem(item=animations.move_down, loops=1, scale=1, text="Move down (full)"),
        # PlaybookItem(item=positions.mid, time_s=5, text="Return to mid"),
        PlaybookItem(item=animations.left_right, loops=1, scale=1, text="High flap (2x)", starting_position=positions.zero),
        PlaybookItem(item=positions.mid, time_s=5, text="Return to mid"),
        PlaybookItem(item=animations.flap_animation,loops=2, scale=.5, text="Low flap (2x)"),
    ]
)

def reset_to_zero():
    positions.zero.play(motors, dmx, hold=5)

atexit.register(reset_to_zero)

if cli_args.live_move:
    positions.lean_left.play(motors, dmx, hold=5, override_speeds=slow_speeds)
    mover(motors, dmx)
elif cli_args.animation_frames:
    animations.flap_animation.stepThrough(motors, dmx, starting_position=positions.zero)
elif cli_args.play:
    animations.flap_animation.play(motors, dmx, starting_position=positions.zero, loops=2)
else:
    playbook.play(motors, dmx)
