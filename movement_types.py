from dataclasses import dataclass
from typing import Dict, List, Tuple
import enum
import time
from stupidArtnet import StupidArtnet

POSITION_CHANNEL = 6 - 1 # channel 0indexed
SPEED_CHANNEL = 7 - 1 # channel 0indexed

BROADCAST_IP = "192.168.0.255"

# Body part
class BP(enum.Enum):
    nose = "nose"
    head = "head"
    body = "body"
    tail = "tail"
    ltw = "left wing tip"
    lmw = "left middle wing"
    liw = "left inner wing"
    rtw = "right wing tip"
    rmw = "right middle wing"
    riw = "right inner wing"


@dataclass
class Motor:

    address: int
    base_offset: int
    current_pos: int = 0
    new_position: int = 0

    def setMovement(self, position, absolute=False):

        if absolute:
            self.new_position = position
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

    def __init__(self):
        self.node = StupidArtnet(target_ip=BROADCAST_IP, universe=0,packet_size=512,fps=30,broadcast=True)

    def sendPositions(self, motors: Dict[BP, Motor]):

        packet = bytearray(512)

        for m in motors.values():
            start_channel = m.address - 1 # 0indexed
            packet[start_channel + POSITION_CHANNEL] = m.new_position
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