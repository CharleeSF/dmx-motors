from movement_types import BP
from position import Position
from animation import Animation, AnimationFrame

from positions import wings_up, wings_down, start_fly, end_fly

in_out_delays = {
    BP.nose: 0,
    BP.head: 0,
    BP.body: 0,
    BP.tail: .6,
    BP.l_wingtip: .6,
    BP.l_wingmid: .4,
    BP.l_winginner: .2,
    BP.r_winginner: .2,
    BP.r_wingmid: .4,
    BP.r_wingtip: .6,
}

# The values are added to the starting position
# Values are in  percentage of movement range (offset - max_value)
flap_animation = Animation(
    [
        AnimationFrame(start_fly, delays=in_out_delays),
        AnimationFrame(wings_up, delays=in_out_delays),
        AnimationFrame(wings_down, delays=in_out_delays),
        AnimationFrame(end_fly, delays=in_out_delays),
    ],
)
