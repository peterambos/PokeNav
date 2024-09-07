import json
from os.path import join

def deduplicate_warps(base_data_path: str) -> list:
    """
    Deduplicates the warps from the warpMap.json file.

    Args:
        base_data_path (str): The path to the base data directory.
        
    Returns:
        list: A list of deduplicated warps.
    """

    with open(join(base_data_path, 'warpMap.json'), 'r', encoding='utf-8') as f:
        raw_warps = json.load(f)

    unique_warps = []
    for warp in raw_warps:
        if not any(
            unique_warp['MapId'] == warp['MapId'] and
            unique_warp['DestinationMap'] == warp['DestinationMap']
            for unique_warp in unique_warps
        ):
            unique_warps.append(warp)

    return unique_warps


def simplify_warps(deduplicated_warps: list, simplified_locations: list) -> list:
    """Simplify the deduplicated warps by extracting the relevant information for graph generation.

    Args:
        deduplicated_warps (list): The list of deduplicated warps.
        simplified_locations (list): The list of simplified locations.

    Returns:
        list: A list of simplified warps with the keys "id", "origin", "originId", "standardTarget", "standardTargetId", and "isLocked".
    """

    simplified_warps = []
    for warp in deduplicated_warps:
        simplified_warp = {
            "id": f"HOE-W-{str(len(simplified_warps)).zfill(4)}",
            "origin": warp["MapId"],
            "originId": next(
                (location["id"] for location in simplified_locations if location["MapId"] == warp["MapId"]),
                None
            ),
            "standardTarget": warp["DestinationMap"],
            "standardTargetId": next(
                (location["id"] for location in simplified_locations if location["MapId"] == warp["DestinationMap"]),
                None
            ),
            "isLocked": warp["IsLocked"]
        }
        simplified_warps.append(simplified_warp)

    return simplified_warps
