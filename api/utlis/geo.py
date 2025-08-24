import math
from typing import Callable, Dict, List, Tuple, TypeVar

T = TypeVar("T")  # Generic type for model


def haversine_distance_between_points(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    R = 6378  # Radius of the Earth in kilometers
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)
    d = (
        math.acos(
            math.sin(p1) * math.sin(p2)
            + math.cos(p1) * math.cos(p2) * math.cos(delta_lambda)
        )
        * R
    )
    return d


def cosine_distance_between_points(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    R = 6371000  # Radius of the Earth in meters
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    delta_phi = p2 - p1
    delta_lambda = math.radians(lon2 - lon1)
    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(p1) * math.cos(p2) * math.sin(delta_lambda / 2) ** 2
    )
    d = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)) * R
    return d


def find_nearest(
    locations: List[T],
    reference: Dict[str, float],
    df: Callable[
        [float, float, float, float], float
    ] = haversine_distance_between_points,
    location_extract_method: Callable[[T], Tuple[float, float]] = lambda loc: (
        loc["lat"],
        loc["lon"],
    ),
) -> Tuple[T, float]:
    min_dist = float("inf")
    nearest = None

    for loc in locations:
        lat, lon = location_extract_method(loc)
        dist = df(reference["lat"], reference["lon"], lat, lon)
        if dist < min_dist:
            min_dist = dist
            nearest = loc

    return nearest, min_dist
