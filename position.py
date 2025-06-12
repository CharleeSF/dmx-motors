from typing import Dict, Optional
from dataclasses import dataclass
from movement_types import BP, Motor
from DMX import DMX
import time


@dataclass
class Position:

    motor_positions: Dict[BP, int]
    absolute: bool = False

    def __post_init__(self):
        # Check ranges here
        pass

    def play(self, motors: Dict[BP, Motor], dmx: DMX, delay: Optional[int] = None):

        start = time.time()

        self.setMotors(motors)
        dmx.sendPositions(motors)

        if delay is not None:
            leftover_sleep = delay - (time.time() - start)
            if leftover_sleep > 0:
                logger.info("Sleeping for %f seconds", leftover_sleep)
                time.sleep(leftover_sleep)

    def setMotors(self, motors: Dict[BP, Motor]):
        for bodypart, position in self.motor_positions.items():
            motors[bodypart].setMovement(position, absolute=self.absolute)

    @classmethod
    def getFromMotors(cls, motors: Dict[BP, Motor]):
        """
        Return a Position object with values thar are currently
        stored on the Motor objects
        """
        
        bp_positions = {}
        for bodypart, motor in motors.items():
            bp_positions[bodypart] = motor.current_pos
        return cls(bp_positions, absolute=True)

    @classmethod
    def addRelative(cls, starting_pos: "Position", relative_pos: "Position", scale: float=1.0):
        """
        Add a relative position to a starting position
        """
        bp_positions = {}
        for bodypart, distance in relative_pos.motor_positions.items():
            bp_positions[bodypart] = starting_pos.motor_positions[bodypart] + int(distance * scale)
        return Position(bp_positions, absolute=True)