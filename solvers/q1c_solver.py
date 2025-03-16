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
    time_limit = 9.8  # Leave some buffer before the 10s timeout

    return depth_first_search(problem, start_time, time_limit)

def astar_search(problem: q1c_problem, start_time, time_limit):
    
    # initialize!
    start_state = problem.getStartState()
    # print(start_state.getNumFood())
    food_grid = start_state.getFood()
    food_positions = tuple((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])
    
    if not food_positions:
        return []
    
    queue = util.PriorityQueue()
    visited = set()
    queue.push((start_state, [], 0, food_positions), 0)
    
    best_solution = []
    max_food_collected = 0
    
    # loop body!
    while not queue.isEmpty():
        # Check if time is up
        if time.time() - start_time > time_limit:
            return best_solution 
        
        # 这里必须要用局部变量 remain_food_positions！！！ 
        # 否则A* 搜索会认为 其他路径也已经吃掉这个食物点，从而导致搜索提早终止
        state, actions, cost, remain_food_positions = queue.pop()
        pacman_position = state.getPacmanPosition()
        
        if (pacman_position, remain_food_positions) in visited:
            continue
        visited.add((pacman_position, remain_food_positions))
        
        collected_food = len(food_positions) - len(remain_food_positions)
        if collected_food > max_food_collected:
            max_food_collected = collected_food
            best_solution = actions
        
        if not remain_food_positions:
            return actions  # Return immediately if all food is collected
        
        for successor, action, step_cost in problem.getSuccessors(state):
            successor_position = successor.getPacmanPosition()
            new_cost = cost + step_cost

            new_remaining_food = tuple(pos for pos in remain_food_positions if pos != successor_position)
            priority = new_cost + heuristic_function(successor_position, new_remaining_food)
            queue.push((successor, actions + [action], new_cost, new_remaining_food), priority)
    
    return best_solution  


def heuristic_function(pacman_position, food_positions):
    if not food_positions:
        return 0
    return min(util.manhattanDistance(pacman_position, food) for food in food_positions)

def depth_first_search(problem, start_time, time_limit):
    """ Implements depth-first search to maximize food collection within the time limit. """
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

# python pacman.py -l layouts/q1c_oddSearch.lay -p SearchAgent -a fn=q1c_solver,prob=q1c_problem --timeout=10