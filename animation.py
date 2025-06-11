from dataclasses import dataclass
from mover import mover
from typing import Dict, List, Tuple, Optional
import time
import msvcrt
import logging

logger = logging.getLogger(__name__)

from movement_types import Position, Motor, BP, DMX

def get_pos_dict(motors: Dict[BP, Motor]):

    return { bodypart : motor.current_pos for bodypart, motor in motors.items()}

@dataclass
class Animation:

    # A list with positions and wait times
    relative_positions: List[Position]

    def getAbsolutePositions(self, starting_position: Position):

        positions = []
        for position in self.relative_positions:
            positions.append(
                Position.addRelative(starting_position, position)
            )
        
        # Don't return the first one, this was the starting position before the animation started
        return positions

    def play(self, motors: Dict[BP, Motor], dmx: DMX, time_s: int = 60):

        start = time.time()
        finished = False
        while not finished:

            for pos in self.positions:
                pos.setMotors(motors)
                dmx.sendPositions(motors)
                time.sleep(pos.delay)

                if (time.time() - start) > time_s:
                    finished = True
                    break
    
    def stepThrough(self, motors: Dict[BP, Motor], dmx: DMX, starting_position: Optional[Position] = None):

        print("Press 's' to go to next frame, 'a' for previous, press 'm' to quit:")

        if not starting_position:
            starting_position = Position.getFromMotors(motors)

        absolute_positions = self.getAbsolutePositions(starting_position)

        position_index = -1
        while True:
            char = msvcrt.getch().decode('utf-8')
            print(f'You pressed: {char!r}')

            if char == 'm':
                break
            elif char == 'a':
                if position_index < 0:
                    raise ValueError("There is no previous frame to go to")
                position_index += 1
            elif char == 's':
                if position_index == len(absolute_positions) - 1:
                    position_index = 0
                else:
                    position_index += 1
            elif char == 'l':
                mover(motors, dmx)
                continue
            else:
                print(f'That key is not a valid command, try again')
                continue
            
            logger.info("Position index: %d", position_index)
            position = absolute_positions[position_index]
            position.setMotors(motors)
            dmx.sendPositions(motors)

            print("\nFinal positions:")
            for bodypart, motor in motors.items():
                print(f'{bodypart}: {motor.getCurrentPos()},')
