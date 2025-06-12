from dataclasses import dataclass
import enum
import logging
from typing import Dict
import msvcrt

from movement_types import BP, Motor
from DMX import DMX

logger = logging.getLogger(__name__)

class UpOrDown(enum.Enum):

    UP = "up"
    DOWN = "down"

@dataclass
class Cmd:

    bodypart: BP
    up_or_down: UpOrDown

cmds = {
    # UP commands
    "q" : Cmd(BP.nose, UpOrDown.UP),
    "w" : Cmd(BP.head, UpOrDown.UP),
    "e" : Cmd(BP.body, UpOrDown.UP),
    "r" : Cmd(BP.tail, UpOrDown.UP),
    "t" : Cmd(BP.l_wingtip, UpOrDown.UP),
    "y" : Cmd(BP.l_wingmid, UpOrDown.UP),
    "u" : Cmd(BP.l_winginner, UpOrDown.UP),
    "i" : Cmd(BP.r_winginner, UpOrDown.UP),
    "o" : Cmd(BP.r_wingmid, UpOrDown.UP),
    "p" : Cmd(BP.r_wingtip, UpOrDown.UP),

    # DOWN commands
    "a" : Cmd(BP.nose, UpOrDown.DOWN),
    "s" : Cmd(BP.head, UpOrDown.DOWN),
    "d" : Cmd(BP.body, UpOrDown.DOWN),
    "f" : Cmd(BP.tail, UpOrDown.DOWN),
    "g" : Cmd(BP.l_wingtip, UpOrDown.DOWN),
    "h" : Cmd(BP.l_wingmid, UpOrDown.DOWN),
    "j" : Cmd(BP.l_winginner, UpOrDown.DOWN),
    "k" : Cmd(BP.r_winginner, UpOrDown.DOWN),
    "l" : Cmd(BP.r_wingmid, UpOrDown.DOWN),
    ";" : Cmd(BP.r_wingtip, UpOrDown.DOWN),
}

def get_pos_dict(motors: Dict[BP, Motor]):

    return { bodypart : motor.current_pos for bodypart, motor in motors.items()}

def print_values(motors: Dict[BP, Motor], starting_position):
    print("\nFinal positions:")
    for bodypart, motor in motors.items():
        print(f'{bodypart}: {motor.getCurrentPos()},')

    print("\nPositions relative to starting position:")
    final_position = get_pos_dict(motors)
    for bodypart in motors.keys():
        start = starting_position[bodypart]
        final = final_position[bodypart]

        print(f"{bodypart}: {final - start},")

def mover(motors: Dict[BP, Motor], dmx: DMX):

    starting_position = get_pos_dict(motors)

    print("Press keys (press 'm' to quit):")
    while True:
        char = msvcrt.getch().decode('utf-8').lower()
        print(f'You pressed: {char!r}')

        if char == 'm':
            break

        elif char == "n":
            print_values(motors, starting_position)

        else:
            try:
                command = cmds[char]
            except KeyError:
                print(f'That key is not a valid command')
                break
            
            motor = motors[command.bodypart]
            if command.up_or_down == UpOrDown.UP:
                logger.info("Moving %s up", command.bodypart)
                motor.decrementByOne()
            elif command.up_or_down == UpOrDown.DOWN:
                logger.info("Moving %s down", command.bodypart)
                motor.incrementByOne()
            
            dmx.sendPositions(motors, override_speeds={bp : 100 for bp in motors.keys()})

