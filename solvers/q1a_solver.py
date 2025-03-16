#---------------------#
# DO NOT MODIFY BEGIN #
#---------------------#

import logging

import util
from problems.q1a_problem import q1a_problem

def q1a_solver(problem: q1a_problem):
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
        self.food_positions = None

def astar_initialise(problem: q1a_problem):
    # YOUR CODE HERE
    astarData = AStarData()
    state = problem.getStartState()
    astarData.start_state = state
    
    food_grid = state.getFood()
    astarData.food_positions = [(x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y]]
    astarData.food_positions = astarData.food_positions[0]

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
    if pacman_position in astarData.visited:
        return False, None
    
    astarData.visited.add(pacman_position)
    
    # Check if the goal is reached
    if problem.isGoalState(state):
        # print('food is here!!!!!!!!')
        return True, actions
    
    # print(state.explored)

    for successor, action, step_cost in problem.getSuccessors(state):
        # print(successor.explored)
        if successor.getPacmanPosition() not in astarData.visited:
            new_cost = cost + step_cost
            priority = new_cost + astar_heuristic(successor.getPacmanPosition(), astarData.food_positions)
            astarData.queue.push((successor, actions + [action], new_cost), priority)
    
    return False, None

def astar_heuristic(pacman_position, food_positions):
    # YOUR CODE HERE        
    
    return util.manhattanDistance(pacman_position, food_positions)

    # python pacman.py -l layouts/q1a_bigMaze2.lay -p SearchAgent -a fn=q1a_solver,prob=q1a_problem --timeout=1
