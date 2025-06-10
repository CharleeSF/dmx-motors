from dataclasses import dataclass
from typing import Dict, List, Tuple
import enum
import time
import logging

from stupidArtnet import StupidArtnet

POSITION_CHANNEL = 6 - 1 # channel 0indexed
SPEED_CHANNEL = 7 - 1 # channel 0indexed

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
    base_offset: int
    current_pos: int = 0
    new_position: int = 0

    def setMovement(self, position, absolute=False):

        if absolute:
            self.new_position = self.base_offset + position
        else:
            self.new_position = self.current_pos + position

        self.speed = self.calculateSpeed(position)

    def calculateSpeed(self, new_position):
        # TODO calculate
        return 0

    def updateCurrentPos(self):
        self.current_pos = self.new_position


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

class DMX:

    def __init__(self, max_pos_value = 60):
        self.max_pos_value = max_pos_value
        self.node = StupidArtnet(target_ip=BROADCAST_IP, universe=0,packet_size=512,fps=30,broadcast=True)

    def sendPositions(self, motors: Dict[BP, Motor]):

        packet = bytearray(512)

        for m in motors.values():
            start_channel = m.address - 1 # 0indexed
            position = m.new_position
            if position < 0:
                logger.warning("Position < 0! %d", position)
                position = 0
            elif position > self.max_pos_value:
                logger.warning("Postiion > max value (%d)! (is %d)", self.max_pos_value, position)
                position = self.max_pos_value

            packet[start_channel + POSITION_CHANNEL] = position
            packet[start_channel + SPEED_CHANNEL] = m.speed
        
        self.node.set(packet)
        self.node.show()

        for m in motors.values():
            m.updateCurrentPos()


@dataclass
class Animation:

    # A list with positions and wait times
    positions: List[Tuple[Position, int]]

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