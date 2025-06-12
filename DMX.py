from typing import Dict, Optional
from movement_types import Motor, BP
from stupidArtnet import StupidArtnet

import logging
logger = logging.getLogger(__name__)

BROADCAST_IP = "192.168.0.255"
POSITION_CHANNEL = 6 - 1 # channel 0indexed
SPEED_CHANNEL = 7 - 1 # channel 0indexed

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

        # Motor.calculateMotorSpeeds(motors)

        dmx_positions = []
        dmx_speeds = []
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
            dmx_value_speed = self.getDmxValueSpeed(m.speed)

            dmx_positions.append(dmx_value_position)
            dmx_speeds.append(dmx_value_speed)

            packet[start_channel + POSITION_CHANNEL] = dmx_value_position
            packet[start_channel + SPEED_CHANNEL] = dmx_value_speed
        
        logger.info("Motor speeds: %s", [m.speed for m in motors.values()])
        logger.info("Motor positions: %s", [m.new_position for m in motors.values()])
        logger.info("DMX positions: %s", dmx_positions)
        logger.info("DMX speeds: %s", dmx_speeds)

        self.node.set(packet)
        self.node.show()

        for m in motors.values():
            m.updateCurrentPos()