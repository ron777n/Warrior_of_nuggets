from typing import Optional

import pymunk


def ray_trace(space, spawn, angle, shape_filter=pymunk.ShapeFilter()):
    if isinstance(angle, pymunk.Vec2d):
        vector = angle
    else:
        vector = pymunk.Vec2d(1, 0).rotated_degrees(angle)
    got = sorted(space.segment_query(spawn, tuple(spawn + vector.scale_to_length(1000)), 3, shape_filter),
                 key=lambda x: abs(x.point - spawn))
    return got


def ray_trace_first(space, spawn, angle, target_filter) -> Optional[pymunk.SegmentQueryInfo]:
    if isinstance(target_filter, pymunk.ShapeFilter):
        target = None
    else:
        target = target_filter
        target_filter = pymunk.ShapeFilter()
    got = ray_trace(space, spawn, angle, target_filter)
    for hit in got:
        if hit.shape.body is target:
            continue
        return hit
    else:
        return None
