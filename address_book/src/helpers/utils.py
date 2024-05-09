import math

from src.helpers.crud_base import CrudBase
from src.models.model import Address
from sqlalchemy.orm import Session
from sqlalchemy import and_


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth specified in decimal degrees.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in kilometers. Use 3956 for miles
    radius_earth = 6371
    distance = radius_earth * c
    return distance


def find_coordinates_within_radius(
    target_lat: float, target_lon: float, address_list: Address, radius: float
) -> list:
    """
    Find all coordinates within a given radius from a target coordinate
    """
    within_radius = []
    for address in address_list:
        if address.latitude != target_lat or address.longitude != target_lon:
            distance = haversine(
                target_lat, target_lon, address.latitude, address.longitude
            )
            if distance <= radius:
                within_radius.append(address)
    return within_radius


def is_duplicate_lat_long(
    crud_obj: CrudBase,
    db: Session,
    latitude: float,
    longitude: float,
    instance_id: int = None,
):
    """
    Check if an address with the given latitude and longitude already exists.
    """
    existing_address = crud_obj.get(
        db,
        query_filter=and_(Address.latitude == latitude, Address.longitude == longitude),
    )
    if existing_address and instance_id:
        return existing_address.id != instance_id
    return existing_address is not None
