from dataclasses import dataclass


@dataclass
class Face:
    x: int
    y: int
    height: int
    width: int
    x_channel = -1
    y_channel = -1
    flagged = False



