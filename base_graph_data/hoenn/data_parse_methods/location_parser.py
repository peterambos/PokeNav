
def simplify_locations(raw_locations: list) -> list:
    """
    Takes a list of location data and simplifies it into a list of dictionaries
    with id, MapId, name, and games keys.

    Args:
        raw_locations (list): A list of dictionaries, each representing a location.

    Returns:
        simplified_locations (list): A list of dictionaries, each representing a location,
                                     containing the id, MapId, name, and games of a location.
    """
    simplified_locations = []
    for location in raw_locations:
        simplified_locations.append(
            {
                "id": f"HOE-L-{str(len(simplified_locations)).zfill(4)}",
                "MapId": location["id"],
                "name": location["name"],
                "games": ["EMRL"],
            }
        )

    return simplified_locations
