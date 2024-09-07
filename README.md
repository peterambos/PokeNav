## Table of Contents <!-- omit in toc -->
- [1. Introduction](#1-introduction)
- [2. Implementation](#2-implementation)
- [3. Data](#3-data)
  - [3.1. Sourcing](#31-sourcing)
  - [3.2. Processing](#32-processing)
    - [3.2.1. Raw Data Parsing](#321-raw-data-parsing)
  - [3.3. Simplified Data Structures](#33-simplified-data-structures)
    - [3.3.1. simplified locations](#331-simplified-locations)
    - [3.3.2. simplified warps](#332-simplified-warps)
    - [3.3.3. simplified connections](#333-simplified-connections)
  - [3.4. Graph Data](#34-graph-data)

# 1. Introduction
This is a Pokémon randomizer warp/door tracker connection and guiding tool.

*It is also a side & passion project and a first foray into full-stack web dev by someone who is **not** a dev or CS student, so please, bear with me here.*

With more and more people trying out randomizer mods for Pokémon games, this project strives to build a web app to fix the *where the hell are all these doors going* and *how the hell do I get back to the next gym/E4 member/story beat* feeling. Basically, users should be able to track the links between doors and warp points, and get a route (when available) of how to get from A to B.

# 2. Implementation
The backend is going to be built with [Django](https://www.djangoproject.com/) and the [Django REST Framework](https://www.django-rest-framework.org/), while a [Vite](https://vitejs.dev/) & [Vue.js](https://vuejs.org/) implementation handles the frontend. Connection data is planned to be stored as graph data, using [NetworkX](https://networkx.org/) graphs stored as JSON files.

# 3. Data
## 3.1. Sourcing
Currently, there is game data available for one Pokémon region: Hoenn, more specifically for the Emerald version of Hoenn. The raw data for this comes from the [repo](https://github.com/darkstormgames/pokeemerald_warpRandomizer/) of the [Pokémon Emerald Randomizer](https://warprandomizer.com/), originally comissioned by online personality [Eric "PointCrow" Morino](https://www.youtube.com/c/pointcrow) and created by [darkstormgames](https://github.com/darkstormgames), [XLuma](https://x.com/TheFanatiker), [AtSign](https://x.com/atsign8877) and [turtleisaac](https://x.com/Turtleisaac) and graciously made available under a GPL-3.0 licence. My deepest thanks go out to them, without their consolidation of the games raw data into a structured format I could go off of, this project would not have been possible.

The used raw data can be found in the `base_graph_data/hoenn/hoenn_data_raw` directory.

## 3.2. Processing
### 3.2.1. Raw Data Parsing
The JSON files from the randomizer repo contains significantly more information than is necessary for the this application, meaning that the data was parsed down into more simplified data structures. This also made data about pre-existing connections between warps and areas more amenable to further processing as graph edges.

The methods used for data processing can be found in the `.py` files in the `base_graph_data/hoenn/data_parse_methods` directory.

Raw location data only had to be simplified down to structured datasets (dictionaries) that only contain the relevant key-value-pairs and a sequential ID. Warp data was treated much the same, just that, as the raw warp data contained duplicate entries for the same warps, a deduplication step had to be performed before simplification.

Preexisting connections, such as walkable transitions between routes which are not randomized, had to be extracted from the raw location data, as these were stored as values of the entries of their locations. This step included a check to make sure that no connection appeared multiple times, as both connected locations contained the connection data, but these would be saved in the graph as only one bidirectional edge.

## 3.3. Simplified Data Structures
All simplified data structures are represented by dictionaries in Python. Prototypes can be found in `base_graph_data/hoenn/prototypes`.

### 3.3.1. simplified locations
| **Key** | **type** | **default**  | **Description**                                                                                                                        |
|---------|----------|--------------|----------------------------------------------------------------------------------------------------------------------------------------|
| id      |   _str_  | "HOE-L-XXXX" | Location ID with sequential numbering (instead of XXXX), beginning at 0000.                                                            |
| name    |   _str_  |      N/A     | Readable name of location.                                                                                                             |
| games   |  _list_  |   ["EMRL"]   | Abbreviation for the games the location appears in. Preparation for future implementation of other Hoenn games like Ruby and Sapphire. |
| MapId   |   _str_  |      N/A     | Map IDs used by raw data structures. Retained for reference and future data implementations.                                           |

### 3.3.2. simplified warps
| **Key**          | **type** | **default**  | **Description**                                                              |
|------------------|----------|--------------|------------------------------------------------------------------------------|
| id               |   _str_  | "HOE-W-XXXX" | Warp ID with sequential numbering (instead of XXXX), beginning at 0000.  |
| origin           |   _str_  |      N/A     | Map ID of warp origin location.                                              |
| originId         |  _list_  |      N/A     | ID of warp origin location.                                                  |
| standardTarget   |   _str_  |      N/A     | Map ID of non-randomized target.                                             |
| standardTargetId |   _str_  |      N/A     | ID of non-randomized target.                                                 |
| isLocked         |  _bool_  |      N/A     | If access to warp is locked by default.                                      |

### 3.3.3. simplified connections
| **Key** | **type** | **default**                    | **Description**                                                                                                                                                                                              |
|---------|----------|--------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| type    |   _str_  | "static" OR "random" OR "warp" | Type of connection. "static" are pre-existing connections between locations. "warp" are connections between warps and their locations. "random" is reserved for user-entered data and not used in base data. |
| nodes   |   _set_  |           {ID1, ID2}           | Set of the IDs of the two connected warps/locations. **WARNING:** _Sets are stored as lists in JSON due to file limitations._                                                                                |
| weight  |   _int_  |                1               | Weight for graph edge for future complex routing implementations.                                                                                                                                            |
## 3.4. Graph Data

The base graph data are implemented as a undirected NetworkX graph, saved as a JSON file. They are mostly organized in the same way as data structures, with the dictionary key-value-pairs being replaced by attribute-value-pairs of the nodes and edges. Locations and warps are stored as nodes and connections are stored as edges. A pre-created JSON representation of the Hoenn base graph data can be found at `base_graph_data/hoenn/hoenn_base_graph.json`. A `.py` file that can be used to restore it from the base data can be found at `base_graph_data/hoenn/data_graph_init.py`. It can also be used to create a JSON of the simplified data pre-graph creation and a PNG plot of the base graph data.

**_command line args/flags of `data_graph_init.py`_**
| **arg/flag**                | **type** | **default**       | **Description**                         |
|-----------------------------|----------|-------------------|-----------------------------------------|
| --base-data-path            |   _str_  | "hoenn_data_raw/" | Path to the base data directory.        |
| --log-simplified-data, -lsd |  _flag_  |        N/A        | Log the simplified data to a JSON file. |
| --json, -j                  |  _flag_  |        N/A        | Output the graph data as a JSON file.   |
| --plot, -p                  |  _flag_  |        N/A        | Plot the data graph as a PNG.           |
| --help, -h                  |  _flag_  |        N/A        | Show a help message and exit.           |
