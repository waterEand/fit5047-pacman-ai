#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1a_problem import q1a_problem
import time

def q1a_solver(problem: q1a_problem):
    start = time.time()
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
    print(time.time() - start)
    return result

#-------------------#
# DO NOT MODIFY END #
#-------------------#

class AStarData:
    # YOUR CODE HERE
    def __init__(self):
        self.queue = util.PriorityQueue()
        self.start_state = None
        self.visited = set()
        self.food_positions = None
        self.g_values = {}
        self.bfs_distances = None

def astar_initialise(problem: q1a_problem):
    # YOUR CODE HERE
    astarData = AStarData()
    state = problem.getStartState()
    astarData.start_state = state
    
    food_grid = state.getFood()
    astarData.food_positions = [(x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y]]
    astarData.food_positions = astarData.food_positions[0]
    
    # astarData.bfs_distances = precompute_bfs(state, astarData.food_positions)  # 计算 BFS 最短路径
    
    # 最少cost 有效减少node expansion
    astarData.g_values[state.getPacmanPosition()] = 0
    
    # astarData.queue.update((state, [], 0), astar_heuristic(state.getPacmanPosition(), astarData.bfs_distances))
    astarData.queue.push((state, [], 0), astar_heuristic(state.getPacmanPosition(), astarData.food_positions))
    
    return astarData

def astar_loop_body(problem: q1a_problem, astarData: AStarData):
    # YOUR CODE HERE
    if astarData.queue.isEmpty():
        # print('Empty!!')
        return True, []  # No solution found

    state, actions, cost = astarData.queue.pop()
    pacman_position = state.getPacmanPosition()
        
    # 这里visited一定要放position！因为state包含其他讯息，误以为某个位置没有访问
    # if pacman_position in astarData.visited:
        # return False, None
    
    # astarData.visited.add(pacman_position)
    astarData.g_values[pacman_position] = cost  # 更新最短路径成本
    
    # Check if the goal is reached
    if problem.isGoalState(state):
        # print('food is here!!!!!!!!')
        return True, actions
    
    # print(state.explored)

    for successor, action, step_cost in problem.getSuccessors(state):
        # print(successor.explored)
        successor_position = successor.getPacmanPosition()
        new_cost = cost + step_cost
        if successor_position not in astarData.g_values or new_cost < astarData.g_values[successor_position]:
        # if successor_position not in astarData.visited:
            # priority = new_cost + astar_heuristic(successor_position, astarData.bfs_distances)
            priority = new_cost + astar_heuristic(successor_position, astarData.food_positions)
            astarData.queue.update((successor, actions + [action], new_cost), priority)
            astarData.g_values[successor_position] = new_cost 
            
    return False, None

def astar_heuristic(pacman_position, food_positions):
    # YOUR CODE HERE        
    
    return util.manhattanDistance(pacman_position, food_positions)

# def astar_heuristic(pacman_position, bfs_distances):
#     # YOUR CODE HERE        
    
#     return bfs_distances.get(pacman_position, float('inf'))  

def precompute_bfs(state, dot_position):
    """
    预先计算每个点到food的距离，考虑wall
    """
    start = time.time()
    walls = state.getWalls()
    width, height = walls.width, walls.height
    bfs_distances = {dot_position: 0}  
    queue = util.Queue()
    queue.push(dot_position)

    while not queue.isEmpty():
        x, y = queue.pop()
        current_dist = bfs_distances[(x, y)]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy

            if 0 <= nx < width and 0 <= ny < height and not walls[nx][ny]:  
                if (nx, ny) not in bfs_distances: 
                    bfs_distances[(nx, ny)] = current_dist + 1
                    queue.push((nx, ny))
    
    print(time.time() - start)

    return bfs_distances

# class AStarData:
#     def __init__(self):
#         self.queue = util.PriorityQueue()
#         self.start_state = None
#         self.visited = set()
#         self.food_position = None

# def astar_initialise(problem: q1a_problem):
#     """ 初始化 A* 搜索 """
#     astarData = AStarData()
#     state = problem.getStartState()
#     astarData.start_state = state
    
#     food_grid = state.getFood()
#     food_positions = [(x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y]]
    
#     if not food_positions:
#         return astarData

#     astarData.food_position = food_positions[0]  # 仅使用最近的食物
#     start_pos = state.getPacmanPosition()
    
#     astarData.queue.push((state, [], 0), astar_heuristic(start_pos, astarData.food_position))
    
#     return astarData

# def astar_loop_body(problem: q1a_problem, astarData: AStarData):
#     """ A* 搜索主循环 """
#     if astarData.queue.isEmpty():
#         return True, []  # No solution found

#     state, actions, cost = astarData.queue.pop()
#     pacman_position = state.getPacmanPosition()
    
#     if pacman_position in astarData.visited:
#         return False, None
    
#     astarData.visited.add(pacman_position)
    
#     if problem.isGoalState(state):
#         return True, actions
    
#     for successor, action, step_cost in problem.getSuccessors(state):
#         successor_position = successor.getPacmanPosition()
#         if successor_position not in astarData.visited:
#             new_cost = cost + step_cost
#             priority = new_cost + astar_heuristic(successor_position, astarData.food_position)
#             astarData.queue.update((successor, actions + [action], new_cost), priority)
            
#     return False, None

# def astar_heuristic(pacman_position, food_position):
#     """ 启发式函数：直接使用曼哈顿距离 """
#     return util.manhattanDistance(pacman_position, food_position)


# python pacman.py -l layouts/q1a_tinyMaze.lay -p SearchAgent -a fn=q1a_solver,prob=q1a_problem --timeout=1
