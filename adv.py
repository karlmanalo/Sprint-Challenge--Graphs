import random

from room import Room
from player import Player
from world import World
from ast import literal_eval

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

# Create player object at starting room
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

"""
NOTE: This code can be made much more DRY, but after finding a working
solution, I got sidetracked using Pandas to find a random seed that
found a path that was less than 970 moves. After finding this seed, I
started to optimize my code, but it messed with the random seed
calculation. I'll go back into this code and optimize it after turning
it in for my SC.
""" 

def traverse_map(player):
    """
    Visits every room in a given world map.
    """

    # Instantiate empty traversal_path and visited set
    traversal_path = []
    visited = set()

    """
    Instantiate empty traversal_stack. This traversal_stack solves the
    crux of our problem, allowing us to keep track of the path we took 
    from a room that had multiple unvisited exits, performing a DFS for
    each exit and keeping track of the path we took to reach a dead
    end.
    """
    traversal_stack = []

    # Define current room as starting room
    current_room = world.rooms[0]

    # While visited set is less than the number of rooms in the world
    while len(visited) < len(world.rooms):
        # Adds current room to visited rooms set
        visited.add(current_room.id)

        """ 
        Empty remaining_choices list for unvisited rooms relative to 
        the current room
        """
        remaining_choices = []

        """
        The following 4 lines of code check if exits exist in all 4
        directions as well as the condition that the subsequent room
        has not already been visited. If both of these conditions are
        met for a room in a given direction, that direction is a 
        candidate that should be added to remaining_choices.
        """
        if current_room.n_to is not None and current_room.n_to.id not in visited:
            remaining_choices.append('n')
        if current_room.s_to is not None and current_room.s_to.id not in visited:
            remaining_choices.append('s')
        if current_room.e_to is not None and current_room.e_to.id not in visited:
            remaining_choices.append('e')
        if current_room.w_to is not None and current_room.w_to.id not in visited:
            remaining_choices.append('w')
        
        # Defining a backtrack dictionary. Will use this when I optimize code.
        backtrack = dict(zip(list("nsew"), list("snwe")))

        """
        If there are no unvisited exits in the current room, we pop the
        last move from our traversal stack and move in the opposite
        direction in order to backtrack. Update current room and append
        this move to our traversal_path.
        """
        if len(remaining_choices) == 0:
            last_move = traversal_stack.pop()
            if last_move == 'n':
                current_room = current_room.s_to
                traversal_path.append('s')
            if last_move == 's':
                current_room = current_room.n_to
                traversal_path.append('n')
            if last_move == 'e':
                current_room = current_room.w_to
                traversal_path.append('w')
            if last_move == 'w':
                current_room = current_room.e_to
                traversal_path.append('e')

        """
        If there are still unvisited exits relative to our current
        room, choose a random exit. Append this choice to both the
        traversal_path and the traversal_stack. Travel in that
        direction.
        """
        if len(remaining_choices) > 0:
            choice = random.choice(remaining_choices)
            traversal_path.append(choice)
            traversal_stack.append(choice)
            if choice == 'n':
                current_room = current_room.n_to
            if choice == 's':
                current_room = current_room.s_to
            if choice == 'e':
                current_room = current_room.e_to
            if choice == 'w':
                current_room = current_room.w_to

    return traversal_path

random.seed(159386)
traversal_path = traverse_map(player)

"""
Shortest Paths:
Seed - Moves
10388 - 975
28187 - 974
58939, 131305, 136067 - 970
159386 - 966
"""

# import pandas as pd

# index = range(150000, 250000)
# columns = ["moves", "path"]

# df = pd.DataFrame(index=index, columns=columns)

# for i in range(150000, 250000):
#     df = df.copy()
#     random.seed(i)
#     traversal_path = traverse_map(player)
#     df["moves"][i] = len(traversal_path)
#     df["path"][i] = traversal_path

# print(df[ df["moves"] == df["moves"].min()])

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")