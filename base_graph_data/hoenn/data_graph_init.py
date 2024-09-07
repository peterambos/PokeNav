import os
from os.path import join
import json
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from data_parse_methods import location_parser, warp_parser, connection_parser

## Parse command line arguments
parser = argparse.ArgumentParser(description="Initialize the data graph from the base data.")
parser.add_argument("--base-data-path", type=str, nargs="?", default="hoenn_data_raw/", help="Path to the base data directory.")
parser.add_argument("--log-simplified-data", "-lsd", action="store_true", help="Log the simplified data to a JSON file.")
parser.add_argument("--json", "-j", action="store_true", help="Output the graph data as a JSON file.")
parser.add_argument("--plot", "-p", action="store_true", help="Plot the data graph as a PNG.")
args = parser.parse_args()

BASE_DATA_PATH = args.base_data_path
LOG_SIMPLIFIED_DATA = args.log_simplified_data
OUTPUT_PLOT_JSON = args.json
OUTPUT_PLOT = args.plot

## Parse Base Data

### Import Raw Location Data

print("Importing raw location data...")

raw_location_data = []
for root_dir, _, files in os.walk(join(BASE_DATA_PATH, "maps")):
    if "map.json" in files:
        with open(join(root_dir, "map.json"), "r", encoding="utf-8") as data_file:
            raw_location_data.append(json.load(data_file))
            
### Import Simplified Data

print("Importing simplified location data...")

simplified_location_data = location_parser.simplify_locations(raw_location_data)

print("Importing deduped and simplified warp data...")

simplified_warp_data = warp_parser.simplify_warps(warp_parser.deduplicate_warps(BASE_DATA_PATH), simplified_location_data)

print("Importing connection data...")

simplified_connection_data = connection_parser.simplify_connections(simplified_location_data, raw_location_data, "static", 1)

print("Parsing complete.")

if LOG_SIMPLIFIED_DATA:
    print("Logging simplified data to file...")
    with open("simplified_data.json", "w", encoding="utf-8") as f:
        json.dump(
            {
                "locations": simplified_location_data,
                "warps": simplified_warp_data,
                "connections": simplified_connection_data
            },
            f,
            ensure_ascii=False,
            indent=4
        )
        

## Generate Graph

print("Generating graph...")

hoenn_base_graph = nx.Graph()

### Init graph location nodes

print("Initializing graph location nodes...")

for location in simplified_location_data:
    hoenn_base_graph.add_node(
        location["id"], 
        MapId=location["MapId"], 
        name=location["name"], 
        games=location["games"]
        )
   
### Init graph warp nodes and their connections to locations
 
print("Initializing graph warp nodes...")

for warp in simplified_warp_data:
    hoenn_base_graph.add_node(
        warp["id"], 
        origin=warp["origin"], 
        originId=warp["originId"], 
        standardTarget=warp["standardTarget"], 
        standardTargetId=warp["standardTargetId"], 
        isLocked=warp["isLocked"]
        )
    hoenn_base_graph.add_edge(
        warp["originId"], warp["id"], 
        type="warp", 
        nodes=[warp["originId"], warp["id"]], 
        weight=1
        )
    
### Init initial connections

print("Initializing initial connections...")

for connection in simplified_connection_data:
    hoenn_base_graph.add_edge(
        connection["nodes"][0], connection["nodes"][1], 
        type=connection["type"], 
        nodes=connection["nodes"], 
        weight=connection["weight"]
        )

print("Graph initialization complete.")

## Export graph data

print("Exporting graph data...")

if OUTPUT_PLOT_JSON:
    with open("hoenn_base_graph.json", "w", encoding="utf-8") as f:
        json.dump(nx.node_link_data(hoenn_base_graph), f, ensure_ascii=False, indent=4)
    print("Graph data exported as hoenn_base_graph.json")
    
if OUTPUT_PLOT:
    plt.figure(figsize=(24, 24), dpi=300)
    nx.draw_spring(hoenn_base_graph, with_labels = True, labels=nx.get_node_attributes(hoenn_base_graph, 'name'))
    plt.savefig("hoenn_base_graph.png")
    print("Graph data plotted as hoenn_base_graph.png")
    
print("Graph data export complete.")
