import pymunk

from .base import BaseObject, block_shape
from .bodies import Solid, DEFAULT_BLOCK_PATH
from .logic import ray_trace, ray_trace_first
from .effects import NoGravity


def exclusion_filter(*shapes: pymunk.Shape | pymunk.Body):
    def _f(shape, query_shape):
        if shape in shapes:
            return False
        return True
    return _f


__all__ = ["BaseObject", "Solid", "ray_trace", "ray_trace_first", "NoGravity", "block_shape", "DEFAULT_BLOCK_PATH",
           "exclusion_filter"]
