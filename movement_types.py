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

    


class DMX:

    def __init__(self, min_pos_dmx=0, max_pos_dmx=60, min_speed_dmx=0, max_speed_dmx=255):
        self.min_pos_dmx = min_pos_dmx
        self.max_pos_dmx = max_pos_dmx
        self.min_speed_dmx = min_speed_dmx
        self.max_speed_dmx = max_speed_dmx
        self.node = StupidArtnet(target_ip=BROADCAST_IP, universe=0,packet_size=512,fps=30,broadcast=True)

    def getDmxValuePosition(self, position: int):

        range = self.max_pos_dmx - self.min_pos_dmx
        relative = round(position / 100 * range)
        return self.min_pos_dmx + relative

    def getDmxValueSpeed(self, speed: int):
        return int(
            self.min_speed_dmx + (self.max_speed_dmx - self.min_speed_dmx) * (speed / 100)
        )

    def sendPositions(self, motors: Dict[BP, Motor]):

        packet = bytearray(512)

        Motor.calculateMotorSpeeds(motors)

        for m in motors.values():
            
            start_channel = m.address - 1 # 0indexed
            
            position = m.new_position
            
            if position < 0:
                logger.warning("DMX: Position < 0! (is %d)", position)
                position = 0
            elif position > 100:
                logger.warning("DMX: Postiion > 100! (is %d)", position)
                position = 100

            dmx_value_position = self.getDmxValuePosition(position)

            packet[start_channel + POSITION_CHANNEL] = dmx_value_position

            # Invert and scale speed for DMX (0=fastest, 255=slowest)
            dmx_value_speed = self.getDmxValueSpeed(m.speed)
            packet[start_channel + SPEED_CHANNEL] = dmx_value_speed
        
        logger.info("Motor speeds: %s", [m.speed for m in motors.values()])
        logger.info("Motor positions: %s", [m.new_position for m in motors.values()])

        self.node.set(packet)
        self.node.show()

        for m in motors.values():
            m.updateCurrentPos()


@dataclass
class Position:

    motor_positions: Dict[BP, int]
    absolute: bool = False

    def __post_init__(self):
        # Check ranges here
        pass

    def play(self, motors: Dict[BP, Motor], dmx: DMX, time_s: Optional[int] = None):
        self.setMotors(motors)
        dmx.sendPositions(motors)
        if time_s is not None:
            time.sleep(time_s)

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