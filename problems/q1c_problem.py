import logging
import time
from typing import Tuple

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState


class q1c_problem:
    """
    A search problem associated with finding a path that collects all of the
    food (dots) in a Pacman game.
    Some useful data has been included here for you
    """
    def __str__(self):
        return str(self.__class__.__module__)

    def __init__(self, gameState: GameState):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.startingGameState: GameState = gameState

    @log_function
    def getStartState(self):
        "*** YOUR CODE HERE ***"
        # return self.startingGameState
        
        position, food_grid = self.startingGameState.getPacmanPosition(), self.startingGameState.getFood()
        food_positions = frozenset((x, y) for x in range(food_grid.width) for y in range(food_grid.height) if food_grid[x][y])
        return (position, food_positions)
        
    @log_function
    def isGoalState(self, state):
        "*** YOUR CODE HERE ***"
        return not state[1]

    @log_function
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """
        "*** YOUR CODE HERE ***"
        # successors = []
        # actions = state.getLegalPacmanActions()
        
        # for action in actions:
        #     successor = state.generatePacmanSuccessor(action)
        #     successors.append((successor, action, 1))
        
        # return successors
        walls = self.startingGameState.getWalls()
        successors = []
        position, foods = state
        x, y = position
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            dx, dy = Actions.directionToVector(action)
            next_x, next_y = int(x + dx), int(y + dy)
            if not walls[next_x][next_y]:
                new_foods = set(foods)
                if (next_x, next_y) in new_foods:
                    new_foods.remove((next_x, next_y))
                new_foods = frozenset(new_foods)
                successor = ((next_x, next_y), new_foods)
                successors.append((successor, action, 1))
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return inf"""
        x, y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 1e7
            cost += 1
        return cost
