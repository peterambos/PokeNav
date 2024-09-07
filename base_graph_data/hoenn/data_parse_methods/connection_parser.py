
def simplify_connections(simplified_locations: list, raw_locations: list, connection_type: str, weight: int) -> list:
    """
    Simplify static connections by replacing MapId's with simplified location id's.
    
    Args:
        simplified_locations (list): A list of dictionaries, each representing a simplified location.
        raw_locations (list): A list of dictionaries, each representing a raw base data location.
        connection_type (str): The type of static connection to simplify.
        weight (int): The weight of the graph edge representing the connection.
        
    Returns:
        connections (list): A list of dictionaries, each representing a simplified connection.
    """
    connections = []
    for raw_location in raw_locations:
        for connection in raw_location.get("connections") or []:
            simplified_connection = {
                "type": connection_type,
                "nodes": [
                    next(
                        (simplified_location["id"] for simplified_location in simplified_locations if simplified_location["MapId"] == connection["map"]),
                        None
                    ),
                    next(
                        (simplified_location["id"] for simplified_location in simplified_locations if simplified_location["MapId"] == raw_location["id"]),
                        None
                    )
                ],
                "weight": weight
            }
            if all(simplified_connection["nodes"]):
                if not any(set(simplified_connection["nodes"]) == set(saved_connection["nodes"]) for saved_connection in connections):
                    connections.append(simplified_connection)

    return connections
