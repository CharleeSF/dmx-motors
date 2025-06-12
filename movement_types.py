from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import enum
import time
import logging
import msvcrt

from stupidArtnet import StupidArtnet

DEFAULT_SPEED = 150

logger = logging.getLogger(__name__)

# Body part
class BP(enum.Enum):
    nose = "nose"
    head = "head"
    body = "body"
    tail = "tail"
    l_wingtip = "left wing tip"
    l_wingmid = "left middle wing"
    l_winginner = "left inner wing"
    r_wingtip = "right wing tip"
    r_wingmid = "right middle wing"
    r_winginner = "right inner wing"


@dataclass
class Motor:

    address: int
    current_pos: int = 0
    new_position: int = 0
    speed: int = DEFAULT_SPEED

    def setMovement(self, position, absolute=False):

        if absolute:
            new_position = position
        else:
            new_position = self.current_pos + position
        
        if new_position > 100:
            logger.warning("New value > 100, refusing")
            new_position = 100
        
        elif new_position < 0:
            logger.warning("New value < 0, refusing")
            new_position = 0
        
        self.new_position = new_position

        self.speed = self.calculateSpeed()

    def incrementByOne(self):
        logger.info("Incrementing %d by 1", self.current_pos)
        position = self.current_pos + 1
        self.setMovement(position, absolute=True)

    def decrementByOne(self):
        logger.info("Decrementing %d by 1", self.current_pos)
        position = self.current_pos - 1
        self.setMovement(position, absolute=True)

    def calculateSpeed(self):
        """
        Calculate speed based on the distance between current_pos and new_position.
        Speed is proportional to the distance, with 0 distance = 0 speed and 100 distance = 100 speed.
        """
        distance = abs(self.current_pos - self.new_position)
        speed = max(0, min(100, int(distance)))
        return speed

    def updateCurrentPos(self):
        self.current_pos = self.new_position
    
    def getCurrentPos(self):
        return self.current_pos

    @classmethod
    def calculateMotorSpeeds(cls, motors: Dict[BP, "Motor"]):
        """
        Set each motor's speed so that all motors reach their new_position at the same time.
        The motor with the largest distance gets speed 100, others are scaled proportionally.
        """
        # Calculate distances for all motors
        distances = {bp: abs(motor.current_pos - motor.new_position) for bp, motor in motors.items()}
        max_distance = max(distances.values()) if distances else 0
        
        for bp, motor in motors.items():
            distance = distances[bp]
            if max_distance == 0:
                logger.warning("Max distance is 0, setting speed to 0")
                motor.speed = 0
            else:
                # Scale so max_distance -> 100, others proportional
                motor.speed = int(100 * distance / max_distance)

    


