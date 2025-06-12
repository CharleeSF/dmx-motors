from dataclasses import dataclass
from mover import mover
from typing import Dict, List, Tuple, Optional
import time
import msvcrt
import logging

logger = logging.getLogger(__name__)

from movement_types import Motor, BP
from position import Position
from DMX import DMX

def get_pos_dict(motors: Dict[BP, Motor]):

    return { bodypart : motor.current_pos for bodypart, motor in motors.items()}

@dataclass
class AnimationFrame:
    relative_position: Position
    hold: Optional[float] = None
    delays: Optional[List[float]] = None
    text: Optional[str] = None
    scale: Optional[float] = None
    loops: Optional[int] = None
    absolute_position: Optional[Position] = None

@dataclass
class Animation:

    # A list with positions and per-step delays
    loop_frames: List[AnimationFrame]
    start_frame: Optional[AnimationFrame] = None
    end_frame: Optional[AnimationFrame] = None

    def setAbsolutePositions(self, motors: Dict[BP, Motor], starting_position: Optional[Position] = None, scale: float = 1.0):
        if not starting_position:
            starting_position = Position.getFromMotors(motors)
        for frame in self.loop_frames:
            frame.absolute_position = Position.addRelative(starting_position, frame.relative_position, scale=scale)
        if self.start_frame:
            self.start_frame.absolute_position = Position.addRelative(starting_position, self.start_frame.relative_position, scale=scale)
        if self.end_frame:
            self.end_frame.absolute_position = Position.addRelative(starting_position, self.end_frame.relative_position, scale=scale)

    def resetAbsolutePositions(self):
        for frame in self.loop_frames:
            frame.absolute_position = None
        if self.start_frame:
            self.start_frame.absolute_position = None
        if self.end_frame:
            self.end_frame.absolute_position = None

    def play(self, motors: Dict[BP, Motor], dmx: DMX, time_s: Optional[int] = None, loops: Optional[int] = None, starting_position: Optional[Position] = None, scale: float = 1.0):
        self.setAbsolutePositions(motors, starting_position, scale)

        start = time.time()
        finished = False

        if self.start_frame:
            self.start_frame.absolute_position.play(motors, dmx, hold=self.start_frame.hold, delays=self.start_frame.delays)

        while not finished:
            if loops is not None and loops <= 0:
                finished = True
                break
            for i, frame in enumerate(self.loop_frames):
                frame.absolute_position.play(motors, dmx, hold=frame.hold, delays=frame.delays)
                if time_s is not None and (time.time() - start) > time_s:
                    finished = True
                    break
            loops -= 1
        
        if self.end_frame:
            self.end_frame.absolute_position.play(motors, dmx, hold=self.end_frame.hold, delays=self.end_frame.delays)

        self.resetAbsolutePositions()

    def stepThrough(self, motors: Dict[BP, Motor], dmx: DMX, starting_position: Optional[Position] = None):
        print("Press 's' to go to next frame, 'a' for previous, press 'm' to quit:")
        self.setAbsolutePositions(motors, starting_position)
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
                if position_index == len(self.loop_frames) - 1:
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
            position = self.loop_frames[position_index].absolute_position
            position.play(motors, dmx, delays=self.loop_frames[position_index].delays)

            print("\nFinal positions:")
            for bodypart, motor in motors.items():
                print(f'{bodypart}: {motor.getCurrentPos()},')
