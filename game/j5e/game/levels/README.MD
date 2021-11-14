-------------------------------------------------
Structure for JSON files describing game levels |
-------------------------------------------------

see 'level_1.json' for a simple example


- level = the grid layout

    - start_point (REQUIRED) = spawning point of lemmings. 4 coordinates : type of segment (line/column/ring), #line, #segment, position on segment. The example in 'level_1.json' has the lemmings spawn on the second pixel of the first segment of the first line.

    - end_point (REQUIRED) = goal for the level = where the lemmings are supposed to arrive to complete the level

    - dimensions = grid dimensions, assuming a 2-D square grid topology

    - hazards = inanimate elements on the grid (obstacles, traps...)

        - walls = block the path and make the lemmings go the opposite way. Position similar to 'start_point', with 2 coordinates instead of 1 to describe the start and end of the wall. The example in 'level_1.json' has a wall on the first segment of the second column, between pixels 12 and 16.

        - reverse_rings = rings where the direction is reversed. By default, agents follow a ring clockwise. The example has the second ring of the first line going counter-clockwise upon startup.


- agents = elements that are moving on the grid "on their own" (lemmings, enemies...)

    - lemmings = agents that spawn at 'start_point' and must go to 'end_point' to complete the level

        - number_spawns = number of lemmings that spawn at the start

        - time_between_spawns = number of seconds between each lemming spawn

        - number_to_win = number of lemmmings that need to read the 'end_point' to complete the level

