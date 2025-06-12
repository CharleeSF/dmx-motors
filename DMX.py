from typing import Dict, Optional
from movement_types import Motor, BP
from stupidArtnet import StupidArtnet

import time
import logging
logger = logging.getLogger(__name__)

BROADCAST_IP = "192.168.0.255"
POSITION_CHANNEL = 6 - 1 # channel 0indexed
SPEED_CHANNEL = 7 - 1 # channel 0indexed

class DMX:

    speed_table = {
        0: 0.08, # second/step
        50: 0.096,
        100: 0.12,
        200: 0.24,
        250: 0.8,
    }

    packet = bytearray(512)

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

        if speed > 100:
            raise ValueError("Speed cannot be greater than 100")
        if speed < 0:
            raise ValueError("Speed cannot be less than 0")
        
        if speed == 0:
            return self.min_speed_dmx
        
        if speed == 100:
            return self.max_speed_dmx

        speed_range = self.min_speed_dmx - self.max_speed_dmx
        speed_relative = speed / 100
        relative_dmx_speed = speed_relative * speed_range
        dmx_speed = self.min_speed_dmx - relative_dmx_speed
        logger.info("Getting speed for %d, relative speed: %f, relative dmx speed: %f, dmx speed: %d", speed, speed_relative, relative_dmx_speed, dmx_speed)
        return int(dmx_speed)

    def findNeartestSpeedKey(self, dmx_speed: int):
        """
        Find the speed on the speed table that is closest under the given speed
        So that means it rounds "up" to fastness
        """
        for speed in sorted(self.speed_table.keys(), reverse=True):
            if speed <= dmx_speed:
                return speed
        
        raise RuntimeError("Did not find speed for %d", dmx_speed)

    def sendPositions(self, motors: Dict[BP, Motor], delays: Optional[dict] = None):

        # Motor.calculateMotorSpeeds(motors)

        dmx_positions = {}
        dmx_speeds = {}
        seconds = {}

        # Use the passed-in delays dict, or default to no delays
        delay_table = delays if delays is not None else {}
        # First calculate
        for bodypart, motor in motors.items():

            current_position = motor.current_pos
            new_position = motor.new_position

            if new_position < 0:
                logger.warning("DMX: Position < 0! (is %d)", new_position)
                new_position = 0
            elif new_position > 100:
                logger.warning("DMX: Postiion > 100! (is %d)", new_position)
                new_position = 100

            dmx_value_current_position = self.getDmxValuePosition(current_position)
            dmx_value_new_position = self.getDmxValuePosition(new_position)
            dmx_value_speed = self.findNeartestSpeedKey(self.getDmxValueSpeed(motor.speed))
            total_steps = abs(dmx_value_new_position - dmx_value_current_position)
            seconds[bodypart] = total_steps * self.speed_table[dmx_value_speed]
            logger.info("Motor %s: %d steps, %f seconds", bodypart, total_steps, seconds[bodypart])

            dmx_positions[bodypart] = dmx_value_new_position
            dmx_speeds[bodypart] = dmx_value_speed
        
        logger.info("Motor speeds: %s", [m.speed for m in motors.values()])
        logger.info("Motor positions: %s", [m.new_position for m in motors.values()])
        logger.info("DMX positions: %s", dmx_positions.values())
        logger.info("DMX speeds: %s", dmx_speeds.values())
        logger.info("Seconds original: %s", seconds.values())

        for bodypart, delay in delay_table.items():
            seconds[bodypart] += delay

        logger.info("Seconds with delay: %s", seconds.values())

        # Then set
        start = time.time()
        if delay_table:
            time_to_do_movement = max(max(seconds.values()), max(delay_table.values())) - max(delay_table.values())
        else:
            time_to_do_movement = max(seconds.values())
        logger.info("Setting the movement over %f seconds", time_to_do_movement)
        while True:
            for bodypart, motor in motors.items():

                if bodypart in delay_table:
                    if time.time() - start < delay_table[bodypart]:
                        continue

                start_channel = motor.address - 1 # 0indexed
                self.packet[start_channel + POSITION_CHANNEL] = dmx_positions[bodypart]
                self.packet[start_channel + SPEED_CHANNEL] = dmx_speeds[bodypart]
            
            self.node.set(self.packet)
            self.node.show()
            if time.time() - start >= time_to_do_movement:
                break

        for m in motors.values():
            m.updateCurrentPos()