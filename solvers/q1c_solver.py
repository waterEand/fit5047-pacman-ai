#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1c_problem import q1c_problem

#-------------------#
# DO NOT MODIFY END #
#-------------------#

import time
def q1c_solver(problem: q1c_problem):
    # YOUR CODE HERE

    start_time = time.time()
    time_limit = 9.5  # Leave some buffer before the 10s timeout

    return astar_search(problem, compute_sum, start_time, time_limit)

def astar_search(problem: q1c_problem, heuristic, start_time, time_limit):
    start_state = problem.getStartState()
    food_grid = start_state.getFood()
    food_positions = frozenset((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])
    num = start_state.getNumFood() 
    
    if not food_positions:
        return []

    queue = util.PriorityQueue()
    visited = set()
    queue.push((start_state, [], 0, food_positions), 0)

    best_solution = []
    max_food_collected = 0

    while not queue.isEmpty():
        if time.time() - start_time > time_limit:
            print("TIME EXCEED!!!!!!")
            return best_solution 

        state, actions, cost, remaining_food = queue.pop()
        pacman_position = state.getPacmanPosition()

        # 让 `visited` 存 `(位置, 剩余 food 状态)`
        state_key = (pacman_position, remaining_food)
        
        if state_key in visited:
            continue
        visited.add(state_key)

        collected_food = num - len(remaining_food)
        if collected_food > max_food_collected:
            max_food_collected = collected_food
            best_solution = actions
        
        if len(remaining_food) == 0:
            # print("ALL FOUND!!!!!!!!")
            return actions  # 吃完所有 food

        successors = problem.getSuccessors(state)
        
        for successor, action, step_cost in successors:
            successor_position = successor.getPacmanPosition()
            new_cost = cost + step_cost

            new_remaining_food = frozenset(pos for pos in remaining_food if pos != successor_position)

            priority = 0.1 * new_cost + heuristic(successor_position, new_remaining_food) # 不需要加上new_cost了！！因为food分布均匀
            # priority = new_cost

            queue.push((successor, actions + [action], new_cost, new_remaining_food), priority)
    
    return best_solution

def astar_heuristic(pacman_position, bfs_distances):
    # YOUR CODE HERE        
    
    if pacman_position in bfs_distances:
        return bfs_distances[pacman_position]
    
    return min(util.manhattanDistance(pacman_position, food) for food in list(bfs_distances.keys())) 

        


def compute_sum(position, remaining_foods):
    '''每次都去找最近的food！！！'''
    if not remaining_foods:
        return 0
    # total_distance = 0
    # for food in remaining_foods:
    #     dist = simple_dist(position, food)
    #     if dist != float('inf'):  
    #         total_distance += dist
            
    # return - total_distance
    current_pos = position
    remaining = set(remaining_foods)  # 复制一份食物点
    total_dist = 0
    
    while remaining:
        nearest_food = min(remaining, key=lambda f: util.manhattanDistance(current_pos, f))
        total_dist += util.manhattanDistance(current_pos, nearest_food)
        
        current_pos = nearest_food
        remaining.remove(nearest_food)
    
    return total_dist   

def simple_dist(position, food):
    return util.manhattanDistance(position, food)


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

# python pacman.py -l layouts/q1c_bigSearch.lay -p SearchAgent -a fn=q1c_solver,prob=q1c_problem --timeout=10