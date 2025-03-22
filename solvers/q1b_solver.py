#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1b_problem import q1b_problem

def q1b_solver(problem: q1b_problem):
    astarData = astar_initialise(problem)
    num_expansions = 0
    terminate = False
    while not terminate:
        num_expansions += 1
        terminate, result = astar_loop_body(problem, astarData)
    print(f'Number of node expansions: {num_expansions}')
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
        self.actions = []
        self.food_positions = None
        self.g_values = {}
        self.bfs_distances = None

def astar_initialise(problem: q1b_problem):
    # YOUR CODE HERE
    astarData = AStarData()
    state = problem.getStartState()
    astarData.start_state = state
    
    food_grid = state.getFood()
    astarData.food_positions = tuple((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])
    
    astarData.bfs_distances = precompute_bfs(state, astarData.food_positions)

    astarData.g_values[state.getPacmanPosition()] = 0  # 初始位置代价为 0
    # astarData.queue.push((state, [], 0), astar_heuristic(state.getPacmanPosition(), astarData.food_positions))
    astarData.queue.push((state, [], 0), astar_heuristic(state.getPacmanPosition(), astarData.bfs_distances))
    
    return astarData


def astar_loop_body(problem: q1b_problem, astarData: AStarData):
    # YOUR CODE HERE
    
    if astarData.queue.isEmpty():
        # print('Empty!!') 
        return True, []

    state, actions, cost = astarData.queue.pop()

    pacman_position = state.getPacmanPosition()

    # 检查是否访问过并更新 g_values
    if pacman_position in astarData.g_values:
        prev_cost = astarData.g_values[pacman_position]
        if cost > prev_cost:
            # print("$$$$$")
            return False, None  # 如果当前路径更长，就不扩展
    
    astarData.g_values[pacman_position] = cost  # 更新当前最优代价
    
    # if pacman_position in astarData.visited:
    #     return False, None
    
    # # visited 只是一个 set，如果某个 successor 之前访问过，它就不会再扩展，即使当前路径更优！
    # astarData.visited.add(pacman_position)
    
    # if problem.isGoalState(state): # 这句话会变成False，可能是因为pacman在successor那里已经吃到了，自动更新为False
    if pacman_position in astarData.food_positions:
        # print("----------- found one! ------------")
        return  True, actions

    for successor, action, step_cost in problem.getSuccessors(state):
        successor_position = successor.getPacmanPosition()
        new_cost = cost + step_cost

        # 如果 successor 还没访问过，或者有更优路径，就更新
        if successor_position not in astarData.g_values or new_cost < astarData.g_values[successor_position]:
            astarData.g_values[successor_position] = new_cost
            # priority = astar_heuristic(successor_position, astarData.food_positions)
            priority = 0.1*new_cost + astar_heuristic(successor_position, astarData.bfs_distances)
            astarData.queue.update((successor, actions + [action], new_cost), priority)

    # for successor, action, step_cost in problem.getSuccessors(state):
    #     if successor.getPacmanPosition() not in astarData.visited:
    #         new_cost = cost + step_cost
            
    #         priority = new_cost + astar_heuristic(successor.getPacmanPosition(), astarData.food_positions)
    #         astarData.queue.update((successor, actions + [action], new_cost), priority) # push
    
    return False, None


# def astar_heuristic(pacman_position, food_positions):
#     # YOUR CODE HERE
#     if not food_positions:
#         return 0
    
#     return min(util.manhattanDistance(pacman_position, food) for food in food_positions)

def astar_heuristic(pacman_position, bfs_distances):
    # YOUR CODE HERE        
    
    if pacman_position in bfs_distances:
        return bfs_distances[pacman_position]
    return min(util.manhattanDistance(pacman_position, food) for food in list(bfs_distances.keys())) 

def precompute_bfs(state, food_positions):
    """
    预先计算每个点到food的距离，考虑wall
    """
    walls = state.getWalls()
    width, height = walls.width, walls.height
    bfs_distances = {}  
    queue = util.Queue()
    
    for food in food_positions:
        x, y = food
        # if walls[x-1][y] and walls[x][y-1] and walls[x][y+1] and walls[x+1][y]:
            # print('not available')
            # continue
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


# def astar_loop_body(problem: q1b_problem, astarData: AStarData):
#     # YOUR CODE HERE
#     if astarData.queue.isEmpty():
#         # print('Empty!!')
#         # return True, astarData.actions  # 应对有些food吃不到的情况 
#         return True, []

#     state, actions, cost, remain_food_positions = astarData.queue.pop()

#     pacman_position = state.getPacmanPosition()

#     if (pacman_position, remain_food_positions) in astarData.visited:
#         return False, None
    
#     astarData.visited.add((pacman_position, remain_food_positions))
    
#     # if pacman_position in food_positions:
#     #     # print("found one!")
#     #     astarData.actions = actions # 应对有些food吃不到的情况
    
#     # 这里必须要用局部变量 remain_food_positions！！！
#     # 否则A* 搜索会认为 其他路径也已经吃掉这个食物点，从而导致搜索提早终止。
#     remain_food_positions = tuple(pos for pos in remain_food_positions if pos != pacman_position)
    
#     if not remain_food_positions:
#         print('All food found.')
        
#         return True, actions
    
#     # print(state.explored)

#     # Expand the current node
#     for successor, action, step_cost in problem.getSuccessors(state):
#         # print(successor.explored)
#         if (successor.getPacmanPosition(), remain_food_positions) not in astarData.visited:
#             new_cost = cost + step_cost
            
#             # this line reduces # of node expansions.
#             new_remaining_food = tuple(pos for pos in remain_food_positions if pos != successor.getPacmanPosition())
            
#             priority = new_cost + astar_heuristic(successor.getPacmanPosition(), new_remaining_food)
#             # astarData.queue.push((successor, actions + [action], new_cost, remain_food_positions), priority)
#             astarData.queue.update((successor, actions + [action], new_cost, new_remaining_food), priority)
    
#     return False, None

# python pacman.py -l layouts/q1b_mediumCorners.lay -p SearchAgent -a fn=q1b_solver,prob=q1b_problem --timeout=5
