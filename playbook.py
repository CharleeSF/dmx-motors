from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Union
import enum
import time
import logging
import msvcrt

from movement_types import BP, Motor
from position import Position
from DMX import DMX
from animation import Animation

logger = logging.getLogger(__name__)

@dataclass
class PlaybookItem:
    """
    Object holding a series of positions and animations
    """
    item: Union[Position, Animation]
    loops: Optional[int] = 1
    time_s: Optional[int] = None
    scale: Optional[float] = None
    text: Optional[str] = None
    starting_position: Optional[Position] = None

    def play(self, motors: Dict[BP, Motor], dmx: DMX):
        if self.text is not None:
            logger.info(self.text)
        if isinstance(self.item, Position):
            logger.info("Playing position")
            if self.scale is not None:
                raise RuntimeError("Cannot scale position")
            self.item.play(motors, dmx, hold=self.time_s)
        elif isinstance(self.item, Animation):
            logger.info("Playing animation")
            self.item.play(motors, dmx, time_s=self.time_s,loops=self.loops, scale=self.scale, starting_position=self.starting_position)

@dataclass
class Playbook:
    """
    Object holding a series of positions and animations
    """

    playbook: List[PlaybookItem]

    def play(self, motors: Dict[BP, Motor], dmx: DMX, step_through: bool = False):
        for item in self.playbook:
            if step_through:
                input("Press enter to continue...")
            item.play(motors, dmx)