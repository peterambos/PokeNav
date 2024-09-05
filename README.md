# PokeNav
A Pokémon randomizer warp/door tracker and guiding tool.
*Also a side & passion project and a first foray into full-stack web dev by someone who is **not** a dev or CS student, so please, bear with me here*

## Description
With more and more people trying out randomizer mods for Pokémon games, this project strives to build a web app to fix the *where the hell are all these doors going* and *how the hell do I get back to the next gym/E4 member/story beat* feeling. Basically, users should be able to track the links between doors and warp points, and get a route (when available) of how to get from A to B.

## Implementation
The backend is going to be built with Django and the Django REST Framework, while a Vite-Vue.js-Implementation handles the frontend. Connection data is planned to be stored as graph data, with locations and warp points as nodes and connections between them as edges.
