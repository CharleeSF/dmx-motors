from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import enum
import time
import logging
import msvcrt

from stupidArtnet import StupidArtnet

POSITION_CHANNEL = 6 - 1 # channel 0indexed
SPEED_CHANNEL = 7 - 1 # channel 0indexed
DEFAULT_SPEED = 150

# DMX speed value range
MIN_SPEED_DMX = 0   # Fastest
MAX_SPEED_DMX = 255 # Slowest

MIN_SPEED = 200
MAX_SPEED = 100

BROADCAST_IP = "192.168.0.255"

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

        self.speed = self.calculateSpeed(position)

    def incrementByOne(self):
        self.new_position = self.current_pos + 1

    def decrementByOne(self):
        self.new_position = self.current_pos - 1

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
    def calculateMotorSpeeds(motors: Dict[BP, "Motor"]):
        # Calculate max distance
        pass
    

@dataclass
class Position:

    motor_positions: Dict[BP, int]
    absolute: bool = False
    delay: int = 10

    def __post_init__(self):
        # Check ranges here
        pass

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
    def addRelative(cls, starting_pos: "Position", relative_pos: "Position"):
        """
        Add a relative position to a starting position
        """
        bp_positions = {}
        for bodypart, distance in relative_pos.motor_positions.items():
            bp_positions[bodypart] = starting_pos.motor_positions[bodypart] + distance
        return Position(bp_positions, absolute=True)

class DMX:

    def __init__(self, base_offset=0, max_pos_value = 60):
        self.base_offset = base_offset
        self.max_pos_value = max_pos_value
        self.node = StupidArtnet(target_ip=BROADCAST_IP, universe=0,packet_size=512,fps=30,broadcast=True)

    def getDmxValue(self, position: int):

        range = self.max_pos_value - self.base_offset
        relative = round(position / 100 * range)
        return self.base_offset + relative

    def sendPositions(self, motors: Dict[BP, Motor]):

        packet = bytearray(512)

        # Motor.calculateMotorSpeeds(motors)

        for m in motors.values():
            
            start_channel = m.address - 1 # 0indexed
            
            position = m.new_position
            
            if position < 0:
                logger.warning("Position < 0! (is %d)", position)
                position = 0
            elif position > 100:
                logger.warning("Postiion > 100! (is %d)", position)
                position = 100

            dmx_value = self.getDmxValue(position)

            packet[start_channel + POSITION_CHANNEL] = dmx_value

            # Invert and scale speed for DMX (0=fastest, 255=slowest)
            dmx_speed = int(
                MIN_SPEED_DMX + (MAX_SPEED_DMX - MIN_SPEED_DMX) * (m.speed / 100)
            )
            dmx_speed = max(MIN_SPEED_DMX, min(MAX_SPEED_DMX, dmx_speed))
            packet[start_channel + SPEED_CHANNEL] = dmx_speed
        
        self.node.set(packet)
        self.node.show()

        for m in motors.values():
            m.updateCurrentPos()

