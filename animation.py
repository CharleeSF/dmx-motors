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

    # A list with positions and per-step delays
    relative_positions: List[Position]
    delays: List[float]

    def getAbsolutePositions(self, starting_position: Position, scale: float = 1.0) -> list[Position]:
        positions = []
        for position in self.relative_positions:
            positions.append(Position.addRelative(starting_position, position, scale=scale))
        # Don't return the first one, this was the starting position before the animation started
        return positions

    def _get_absolute_positions(
        self,
        motors: Dict[BP, Motor],
        starting_position: Optional[Position] = None,
        scale: float = 1.0
    ) -> list[Position]:
        if starting_position is None:
            starting_position = Position.getFromMotors(motors)
        return self.getAbsolutePositions(starting_position, scale=scale)

    def _apply_position(
        self,
        pos: Position,
        motors: Dict[BP, Motor],
        dmx: DMX
    ) -> None:
        pos.setMotors(motors)
        dmx.sendPositions(motors)

    def play(self, motors: Dict[BP, Motor], dmx: DMX, time_s: Optional[int] = None, loops: Optional[int] = None, starting_position: Optional[Position] = None, scale: float = 1.0):
        absolute_positions = self._get_absolute_positions(motors, starting_position, scale)
        start = time.time()
        finished = False

        self._apply_position(absolute_positions[0], motors, dmx)
        time.sleep(self.delays[0])

        while not finished:
            if loops is not None and loops <= 0:
                finished = True
                break
            for i, pos in enumerate(absolute_positions[1:-1]):
                self._apply_position(pos, motors, dmx)
                time.sleep(self.delays[i])
                if time_s is not None and (time.time() - start) > time_s:
                    finished = True
                    break
            loops -= 1
        
        self._apply_position(absolute_positions[-1], motors, dmx)
        time.sleep(self.delays[-1])

    def stepThrough(self, motors: Dict[BP, Motor], dmx: DMX, starting_position: Optional[Position] = None):
        print("Press 's' to go to next frame, 'a' for previous, press 'm' to quit:")
        absolute_positions = self._get_absolute_positions(motors, starting_position)
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
            self._apply_position(position, motors, dmx)

            print("\nFinal positions:")
            for bodypart, motor in motors.items():
                print(f'{bodypart}: {motor.getCurrentPos()},')
