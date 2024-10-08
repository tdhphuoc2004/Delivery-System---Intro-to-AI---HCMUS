import heapq
from queue import Queue
from Utils import createState
from level1 import reconstruct_path 
from Utils import createState, generateNewState, restore_goal_positions, find_and_set_other_vehicles, restore_vehicle_positions, print_vehicle_status
def heuristic(pos, goal):
  """
  Calculates the Manhattan distance heuristic between two positions.

  Args:
      pos: Starting position (tuple of x, y coordinates).
      goal: Goal position (tuple of x, y coordinates).

  Returns:
      The Manhattan distance between the positions.
  """

  x1, y1 = pos
  x2, y2 = goal
  return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(board, start, goal, initial_fuel, current_fuel):
    frontier = [(0, start, current_fuel)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    fuel_at_node = {start: current_fuel}

    while frontier:
        current_cost, current, fuel = heapq.heappop(frontier)

        if current == goal:
            return reconstruct_path(came_from, start, goal), cost_so_far[goal]

        for neighbor in board.get_neighbors(current):
            new_cost = cost_so_far[current] + board.get_cost(neighbor[0], neighbor[1])
            new_fuel = fuel - 1

            if board.matrix[neighbor[0]][neighbor[1]][0] == 'F':
                new_fuel = initial_fuel

            if new_fuel < 0:
                continue

            if (neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]) and new_fuel >= 0:
                cost_so_far[neighbor] = new_cost
                fuel_at_node[neighbor] = new_fuel
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(frontier, (priority, neighbor, new_fuel))
                came_from[neighbor] = current

    return None, float('inf')

def A_star_search(board, goal, initial_fuel, current_fuel, gas_stations):
    start = board.start_pos
    if not start or not goal:
        return None

    # First, try to find a path directly from start to goal with the initial fuel
    path, total_cost = a_star_search(board, start, goal, initial_fuel, current_fuel)
    if path:
        return path

    # If not enough fuel, try to find the shortest path via gas stations, but if not have gas stations on map then return None 
    if not gas_stations:
        return None

    shortest_path = None
    shortest_cost = float('inf')

    for gas_station in gas_stations:
        # Path from start to gas station
        path_to_gas, cost_to_gas = a_star_search(board, start, gas_station, initial_fuel, current_fuel)
        if not path_to_gas:
            continue

        # Path from gas station to goal after refueling
        path_from_gas, cost_from_gas = a_star_search(board, gas_station, goal, initial_fuel, initial_fuel)
        if not path_from_gas:
            continue

        # Combine both paths and costs
        total_path = path_to_gas + path_from_gas[1:]  # Avoid duplicating the gas station in the path
        total_cost = cost_to_gas + cost_from_gas

        if total_cost < shortest_cost:
            shortest_path = total_path
            shortest_cost = total_cost

    return shortest_path if shortest_cost <= board.time else None


def A_star_search_lv4(boards):
    """
    Performs A* search for multiple vehicles on separate boards with turn-based movement,
    handling collision avoidance and Level 4 cost calculations. The loop continues until
    the main vehicle reaches its goal 'G'.

    Args:
        boards: A list of Board objects, each representing the environment for a vehicle.

    Returns:
        None
    """
    
    # Initialize paths storage
    gas_stations = boards[0].find_gas_locations()
    initial_fuel = boards[0].inital_fuel 
    while True:
        main_vehicle_location = boards[0].find_vehicle()
        x_coord, y_coord = main_vehicle_location
        if x_coord == boards[0].goal_pos[0] and y_coord == boards[0].goal_pos[1]:
            break

        # Update and pass board state between vehicles
        for vehicle_index in range(len(boards)):
            board = boards[vehicle_index]
            fuel = board.fuel
            goal_pos = board.goal_pos
            str_vehicle_index = str(vehicle_index)
            print('Start pos:', board.start_pos)
            print ('End pos:', board.goal_pos)
            print(f"\tTime: {board.time}")
            print(f"\tFuel: {fuel}")
            #Find and set other vehicles' positions to -1
            find_and_set_other_vehicles(board, str_vehicle_index)
            # Construct the path
            path = A_star_search(board, goal_pos, initial_fuel, fuel, gas_stations)
            if path is None and vehicle_index == 0 and (board.fuel == 0 or board.time == 0):
                print(f"Main vehicle cannot find a path to the goal.")
                return 
            elif path is None: 
                print(f"Vehicle {vehicle_index} cannot find a path to the goal.")
                generateNewState(board, vehicle_index, gas_stations,  None)
            else:
                path.pop(0)
                print("Path found in A*:", path)
                move_to = path.pop(0)

                # Generate a new state
                print(f"Move To: {move_to}")
                generateNewState(board, vehicle_index, gas_stations, move_to)

            # # Restore vehicle positions and print status
            restore_vehicle_positions(boards, board)
            print_vehicle_status(board)

            # Restore goal positions for all vehicles
            restore_goal_positions(boards, board, len(boards))

            # Pass the updated state to the next vehicle
            if vehicle_index < len(boards) - 1:
                boards[vehicle_index + 1].matrix = board.matrix 

            # Re-check the main vehicle's position after every move
            main_vehicle_location = boards[0].find_vehicle()
            x_coord, y_coord = main_vehicle_location
            if x_coord == boards[0].goal_pos[0] and y_coord == boards[0].goal_pos[1]:
                break