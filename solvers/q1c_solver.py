#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem
import time

#-------------------#
# DO NOT MODIFY END #
#-------------------#

def q1c_solver(problem: q1c_problem):
    # YOUR CODE HERE

    start_time = time.time()
    time_limit = 9.9  # Leave some buffer before the 10s timeout

    return astar_search(problem, astar_heuristic, start_time, time_limit)
    

# def astar_search(problem: q1c_problem, start_time, time_limit):
#     start_state = problem.getStartState()
#     food_grid = start_state.getFood()
#     food_positions = frozenset((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])

#     if not food_positions:
#         return []
    
#     queue = util.PriorityQueue()
#     visited = set()
#     queue.push((start_state, [], 0), 0)

#     best_solution = []
#     max_food_collected = 0

#     while not queue.isEmpty():
#         if time.time() - start_time > time_limit:
#             print("TIME EXCEED!!!!!!")
#             return best_solution 

#         state, actions, cost = queue.pop()
#         pacman_position = state.getPacmanPosition()

#         # 只存 Pac-Man 位置，减少搜索空间
#         if pacman_position in visited:
#             continue
#         visited.add(pacman_position)

#         collected_food = start_state.getNumFood() - state.getNumFood()
#         if collected_food > max_food_collected:
#             max_food_collected = collected_food
#             best_solution = actions
        
#         if state.getNumFood() == 0:
#             print("ALL FOUND!!!!!!!!")
#             return actions  # Return immediately if all food is collected
        
#         successors = problem.getSuccessors(state)

#         # for successor, action, step_cost in successors:
#         #     successor_position = successor.getPacmanPosition()
#         #     new_cost = cost + step_cost

#         #     # 计算新的剩余食物状态
#         #     new_remaining_food = frozenset(pos for pos in remaining_food if pos != successor_position)

#         #     # 计算启发式
#         #     priority = new_cost + mst_heuristic(successor_position, new_remaining_food, food_positions)
#         #     queue.update((successor, actions + [action], new_cost, new_remaining_food), priority)
    
#         # **只扩展前 K 个最优 successor**
#         K = 3  # 你可以调整这个值
#         sorted_successors = sorted(successors, key=lambda s: fast_heuristic(s[0].getPacmanPosition(), food_positions))[:K]

#         for successor, action, step_cost in sorted_successors:
#             new_cost = cost + step_cost
#             priority = new_cost + fast_heuristic(successor.getPacmanPosition(), food_positions)
#             queue.update((successor, actions + [action], new_cost), priority)
            
#     return best_solution  

# def astar_search(problem: q1c_problem, start_time, time_limit):
#     '''将所有剩余 food 作为状态的一部分，导致状态空间爆炸! 超时！'''
    
#     # initialize!
#     start_state = problem.getStartState()
#     # print(start_state.getNumFood())
#     food_grid = start_state.getFood()
#     food_positions = tuple((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])
    
#     if not food_positions:
#         return []
    
#     queue = util.PriorityQueue()
#     visited = set()
#     queue.push((start_state, [], 0, food_positions), 0)
    
#     best_solution = []
#     max_food_collected = 0
    
#     # loop body!
#     while not queue.isEmpty():
#         # Check if time is up
#         if time.time() - start_time > time_limit:
#             return best_solution 
        
#         # 这里必须要用局部变量 remain_food_positions！！！ 
#         # 否则A* 搜索会认为 其他路径也已经吃掉这个食物点，从而导致搜索提早终止
#         state, actions, cost, remain_food_positions = queue.pop()
#         pacman_position = state.getPacmanPosition()
        
#         if (pacman_position, remain_food_positions) in visited:
#             continue
#         visited.add((pacman_position, remain_food_positions))
        
#         collected_food = len(food_positions) - len(remain_food_positions)
#         if collected_food > max_food_collected:
#             max_food_collected = collected_food
#             best_solution = actions
        
#         if not remain_food_positions:
#             return actions  # Return immediately if all food is collected
        
#         for successor, action, step_cost in problem.getSuccessors(state):
#             successor_position = successor.getPacmanPosition()
#             new_cost = cost + step_cost

#             new_remaining_food = tuple(pos for pos in remain_food_positions if pos != successor_position)
#             priority = new_cost + heuristic_function(successor_position, new_remaining_food)
#             queue.push((successor, actions + [action], new_cost, new_remaining_food), priority)
    
#     return best_solution  

def astar_search(problem: q1c_problem, heuristic, start_time, time_limit):
    start_state = problem.getStartState()
    food_grid = start_state.getFood()
    food_positions = frozenset((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])
    num_food = start_state.getNumFood()
    
    bfs_distances = precompute_bfs(start_state, food_positions)
    
    if not food_positions:
        return []

    queue = util.PriorityQueue()
    visited = set()
    queue.push((start_state, [], 0), 0)

    best_solution = []
    max_food_collected = 0

    while not queue.isEmpty():
        if time.time() - start_time > time_limit:
            print("TIME EXCEED!!!!!!")
            return best_solution 

        state, actions, cost = queue.pop()
        pacman_position = state.getPacmanPosition()

        if pacman_position in visited:
            continue
        visited.add(pacman_position)

        collected_food = num_food - state.getNumFood()
        if collected_food > max_food_collected:
            max_food_collected = collected_food
            best_solution = actions
        
        if state.getNumFood() == 0:
            # print("ALL FOUND!!!!!!!!")
            return actions  

        successors = problem.getSuccessors(state)

        # 只扩展前 K 个最优 successor
        K = 3
        
        sorted_successors = sorted(successors, key=lambda s: heuristic(s[0].getPacmanPosition(), bfs_distances))

        for successor, action, step_cost in sorted_successors:
            successor_position = successor.getPacmanPosition()
            new_cost = cost + step_cost

            priority = new_cost + heuristic(successor_position, bfs_distances)

            queue.update((successor, actions + [action], new_cost), priority)
    
    return best_solution  


def heuristic_function(pacman_position, food_positions):
    if not food_positions:
        return 0
    return min(util.manhattanDistance(pacman_position, food) for food in food_positions)

def fast_heuristic(pacman_position, remaining_food):
    """
    让 PacMan 优先靠近最近的 food
    """
    if not remaining_food:
        return 0

    # 最近的 food 
    min_distance = min(util.manhattanDistance(pacman_position, food) for food in remaining_food)

    return min_distance 

def astar_heuristic(pacman_position, bfs_distances):
    # YOUR CODE HERE        
    
    if pacman_position in bfs_distances:
        return bfs_distances[pacman_position]
    return min(util.manhattanDistance(pacman_position, food) for food in list(bfs_distances.keys())) 


def depth_first_search(problem, start_time, time_limit):
    """ 时间够快 但是cost太大。。。 """
    
    start_state = problem.getStartState()
    food_grid = start_state.getFood()
    walls = start_state.getWalls()
    food_positions = tuple((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])
    
    if not food_positions:
        return []
    # stack = util.Stack
    stack = [(start_state, [], food_positions)]
    visited = set()
    best_solution = []
    max_food_collected = 0
    
    while stack:
        # Check if time is up
        if time.time() - start_time > time_limit:
            return best_solution

        state, actions, remaining_food = stack.pop()
        pacman_position = state.getPacmanPosition()
        
        if (pacman_position, remaining_food) in visited:
            continue
        visited.add((pacman_position, remaining_food))
        
        collected_food = len(food_positions) - len(remaining_food)
        if collected_food > max_food_collected:
            max_food_collected = collected_food
            best_solution = actions
        
        if not remaining_food:
            return actions  # Return immediately if all food is collected
        
        for successor, action, step_cost in problem.getSuccessors(state):
            successor_position = successor.getPacmanPosition()
            new_remaining_food = tuple(pos for pos in remaining_food if pos != successor_position)
            stack.append((successor, actions + [action], new_remaining_food))
    
    return best_solution  # Return best found solution within time limit


def prim_mst(food_positions):
    """
    使用 Prim 算法计算最小生成树（MST）
    """
    if not food_positions:
        return 0

    food_list = list(food_positions)
    mst_cost = 0
    visited = set()
    queue = util.PriorityQueue()

    start = food_list[0]
    visited.add(start)

    for food in food_list[1:]:
        queue.push((start, food), util.manhattanDistance(start, food))

    while not queue.isEmpty() and len(visited) < len(food_list):
        (u, v) = queue.pop()

        if v not in visited:
            visited.add(v)
            mst_cost += util.manhattanDistance(u, v)

            for food in food_list:
                if food not in visited:
                    queue.push((v, food), util.manhattanDistance(v, food))

    return mst_cost

# def mst_heuristic(pacman_position, food_positions):
#     """
#     使用最小生成树 (MST) 
#     """
#     if not food_positions:
#         return 0

#     # 加入 Pac-Man 位置，使其能更快靠近 food
#     all_positions = set(food_positions) | {pacman_position}
    
#     return prim_mst(all_positions)


def precompute_bfs(gameState, food_positions):
    """
    预先计算每个点到food的距离，考虑wall
    """
    walls = gameState.getWalls()
    width, height = walls.width, walls.height
    bfs_distances = {}  
    queue = util.Queue()
    
    for food in food_positions:
        x, y = food
        if walls[x-1][y] and walls[x][y-1] and walls[x][y+1] and walls[x+1][y]:
            # print('not available')
            continue
            # bfs_distances[food] = float('inf')
        bfs_distances[food] = 0
        queue.push(food)
    
    while not queue.isEmpty():
        x, y = queue.pop()
        current_dist = bfs_distances[(x, y)]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]: # 四个方向
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height and not walls[nx][ny]:
                if (nx, ny) not in bfs_distances: 
                    bfs_distances[(nx, ny)] = current_dist + 1
                    queue.push((nx, ny))

    return bfs_distances


# python pacman.py -l layouts/q1c_trickySearch.lay -p SearchAgent -a fn=q1c_solver,prob=q1c_problem --timeout=10