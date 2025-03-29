#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#
from game import Actions, Agent, Directions
import time


# def q1c_solver(problem: q1c_problem):
#     # YOUR CODE HERE

#     start_time = time.time()
#     time_limit = 9.5  # Leave some buffer before the 10s timeout

#     return astar_search(problem, compute_sum, start_time, time_limit)
#     # return greedy_bfs_collect(problem, start_time, time_limit)

# def astar_search(problem: q1c_problem, heuristic, start_time, time_limit):
#     start_state = problem.getStartState()
#     # num = start_state.getNumFood() 
    
#     if problem.isGoalState(start_state):
#         return []

#     queue = util.PriorityQueue()
#     visited = set()
#     queue.push((start_state, [], 0), 0)
#     # print(queue[0])
#     best_solution = []
#     # max_food_collected = 0

#     while not queue.isEmpty():
#         if time.time() - start_time > time_limit:
#             print("TIME EXCEED!!!!!!")
#             return best_solution 
#         state, actions, cost = queue.pop()
#         pacman_position, food_positions = state
#         # pacman_position = state.getPacmanPosition()

#         # 让 `visited` 存 `(位置, 剩余 food 状态)`
#         # state_key = (pacman_position, remaining_food)
        
#         if state in visited:
#             continue
#         visited.add(state)

#         # collected_food = num - len(food_positions)
#         # if collected_food > max_food_collected:
#         #     max_food_collected = collected_food
#         #     best_solution = actions
        
#         if len(food_positions) == 0:
#             print("ALL FOUND!!!!!!!!")
#             return actions  # 吃完所有 food

#         successors = problem.getSuccessors(state)
        
#         for successor, action, step_cost in successors:
#             successor_position, food_positions = successor
#             new_cost = cost + step_cost

#             new_remaining_food = frozenset(pos for pos in food_positions if pos != successor_position)

#             priority = 0.1 * new_cost + heuristic(successor_position, food_positions) # 不需要加上new_cost了！！因为food分布均匀
#             # priority = new_cost

#             queue.push((successor, actions + [action], new_cost), priority)
    
#     return best_solution

# def astar_heuristic(pacman_position, bfs_distances):
#     # YOUR CODE HERE        
    
#     if pacman_position in bfs_distances:
#         return bfs_distances[pacman_position]
    
#     return min(util.manhattanDistance(pacman_position, food) for food in list(bfs_distances.keys())) 


# def compute_sum(position, remaining_foods):
#     '''每次都去找最近的food！！！'''
#     if not remaining_foods:
#         return 0
#     # total_distance = 0
#     # for food in remaining_foods:
#     #     dist = simple_dist(position, food)
#     #     if dist != float('inf'):  
#     #         total_distance += dist
            
#     # return - total_distance
#     current_pos = position
#     remaining = set(remaining_foods)  # 复制一份食物点
#     total_dist = 0
    
#     while remaining:
#         nearest_food = min(remaining, key=lambda f: util.manhattanDistance(current_pos, f))
#         total_dist += util.manhattanDistance(current_pos, nearest_food)
        
#         current_pos = nearest_food
#         remaining.remove(nearest_food)
    
#     return total_dist 

def q1c_solver(problem: q1c_problem):
    start_time = time.time()
    time_limit = 9.5 

    return greedy_bfs_solver(problem, start_time, time_limit)
    # return eat_in_chunks_solver(problem, start_time, time_limit)

def greedy_bfs_solver(problem: q1c_problem, start_time, time_limit):
    start_state = problem.getStartState()
    pacman_pos, food_set = start_state
    food_set = set(food_set)  # 可变集合

    walls = problem.startingGameState.getWalls()
    wall_width = walls.width if hasattr(walls, "width") else len(walls)
    wall_height = walls.height if hasattr(walls, "height") else len(walls[0])

    actions = []

    while food_set:
        if time.time() - start_time > time_limit:
            print("TIME EXCEEDED!!!")
            return actions

        path, target_food = bfs_to_closest_food(pacman_pos, food_set, walls, wall_width, wall_height)

        if path is None or target_food is None:
            break  # 无法到达剩余食物
            
        actions.extend(path)
        pacman_pos = target_food
        food_set.remove(target_food)

    return actions


def bfs_to_closest_food(start_pos, food_set, walls, wall_width, wall_height):
    queue = util.Queue()
    visited = set()
    queue.push((start_pos, []))
    visited.add(start_pos)

    while not queue.isEmpty():
        cur_pos, path = queue.pop()
        if cur_pos in food_set:
            return path, cur_pos  # 早停：一旦找到就返回

        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(direction)
            next_pos = (int(cur_pos[0] + dx), int(cur_pos[1] + dy))

            if not (0 <= next_pos[0] < wall_width and 0 <= next_pos[1] < wall_height):
                continue
            if walls[next_pos[0]][next_pos[1]]:
                continue
            if next_pos not in visited:
                visited.add(next_pos)
                queue.push((next_pos, path + [direction]))

    return None, None

# def bfs_to_closest_food(start_pos, food_set, walls, wall_width, wall_height):
            
#     queue = util.Queue()
#     visited = set()
#     queue.push((start_pos, []))
#     visited.add(start_pos)

#     first_food_path = None
#     first_food_pos = None

#     while not queue.isEmpty():
#         cur_pos, path = queue.pop()

#         if cur_pos in food_set:
#             if is_dead_end(cur_pos, walls, wall_width, wall_height):
#                 return path, cur_pos  # ✅ 优先选择死角上的 food
#             if first_food_path is None:
#                 first_food_path = path
#                 first_food_pos = cur_pos

#         for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
#             dx, dy = Actions.directionToVector(direction)
#             next_pos = (int(cur_pos[0] + dx), int(cur_pos[1] + dy))

#             if not (0 <= next_pos[0] < wall_width and 0 <= next_pos[1] < wall_height):
#                 continue
#             if walls[next_pos[0]][next_pos[1]]:
#                 continue
#             if next_pos not in visited:
#                 visited.add(next_pos)
#                 queue.push((next_pos, path + [direction]))

#     # 如果 BFS 结束都没遇到死角上的 food，就返回第一个遇到的普通 food
#     return first_food_path, first_food_pos

def is_dead_end(pos, walls, width, height):
    count = 0
    for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
        dx, dy = Actions.directionToVector(direction)
        nx, ny = int(pos[0] + dx), int(pos[1] + dy)
        if 0 <= nx < width and 0 <= ny < height and not walls[nx][ny]:
            count += 1
    return count == 1

def bfs_path(start, goal, walls, width, height):
    """返回从 start 到 goal 的动作序列"""
    queue = util.Queue()
    visited = set()
    queue.push((start, []))
    visited.add(start)

    while not queue.isEmpty():
        pos, path = queue.pop()
        if pos == goal:
            return path

        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(direction)
            next_pos = (int(pos[0] + dx), int(pos[1] + dy))
            if not (0 <= next_pos[0] < width and 0 <= next_pos[1] < height):
                continue
            if walls[next_pos[0]][next_pos[1]]:
                continue
            if next_pos not in visited:
                visited.add(next_pos)
                queue.push((next_pos, path + [direction]))
    return None

# def depth_first_search(problem, start_time, time_limit):
#     """ 时间够快 但是cost太大。。。 """
    
#     start_state = problem.getStartState()
#     food_grid = start_state.getFood()
#     walls = start_state.getWalls()
#     food_positions = tuple((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])
    
#     if not food_positions:
#         return []
#     # stack = util.Stack
#     stack = [(start_state, [], food_positions)]
#     visited = set()
#     best_solution = []
#     max_food_collected = 0
    
#     while stack:
#         # Check if time is up
#         if time.time() - start_time > time_limit:
#             return best_solution

#         state, actions, remaining_food = stack.pop()
#         pacman_position = state.getPacmanPosition()
        
#         if (pacman_position, remaining_food) in visited:
#             continue
#         visited.add((pacman_position, remaining_food))
        
#         collected_food = len(food_positions) - len(remaining_food)
#         if collected_food > max_food_collected:
#             max_food_collected = collected_food
#             best_solution = actions
        
#         if not remaining_food:
#             return actions  # Return immediately if all food is collected
        
#         for successor, action, step_cost in problem.getSuccessors(state):
#             successor_position = successor.getPacmanPosition()
#             new_remaining_food = tuple(pos for pos in remaining_food if pos != successor_position)
#             stack.append((successor, actions + [action], new_remaining_food))
    
#     return best_solution  # Return best found solution within time limit

# python pacman.py -l layouts/q1c_mediumSearch.lay -p SearchAgent -a fn=q1c_solver,prob=q1c_problem --timeout=10