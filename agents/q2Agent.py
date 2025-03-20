import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance

import sys


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class Q2_Agent(Agent):

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '3'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        
    # def __init__(self, evalFn='betterEvaluationFunction', depth='3'):
    #     self.index = 0
    #     self.evaluationFunction = util.lookup(evalFn, globals())
    #     self.depth = int(depth)

    @log_function
    def getAction(self, gameState: GameState):
        """
            Returns the minimax action from the current gameState using self.depth
            and self.evaluationFunction.

            Here are some method calls that might be useful when implementing minimax.

            gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

            gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

            gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        logger = logging.getLogger('root')
        logger.info('MinimaxAgent')
        "*** YOUR CODE HERE ***"

        best_action, _ = self.alphaBeta(gameState, depth=self.depth, agentIndex=0, alpha=-float('inf'), beta=float('inf'))
        return best_action
        # return self.minimax(gameState, agentIndex=0, depth=self.depth)[1]


    def alphaBeta(self, gameState, depth, agentIndex, alpha, beta):
        """
        Alpha-Beta Pruning with Minimax.
        """
        # check depth & end of game
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return None, self.evaluationFunction(gameState)

        num_agents = gameState.getNumAgents()
        is_pacman = (agentIndex == 0)

        # best_action = None
        # best_value = -float('inf') if is_pacman else float('inf')

        actions = gameState.getLegalActions(agentIndex)
        if not actions:
            return None, self.evaluationFunction(gameState)
        
        # 随机打乱行动顺序，避免相同分数导致上下循环
        # random.shuffle(actions)
        # action顺序很重要！
        if is_pacman:
            # actions = sorted(
            #     actions, 
            #     key=lambda action: self.evaluationFunction(gameState.generateSuccessor(agentIndex, action)),
            #     # key=lambda a: (self._actionScore(gameState, a), a), 
            #     reverse=True
            # )
            actions = self.rankActions(gameState, actions)
        else:
            random.shuffle(actions)
            # actions = self.rankActions(gameState, actions)

        best_value = -float('inf') if is_pacman else float('inf')
        best_action = actions[0] # 默认选择第一个 action
        
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)

            next_agent = (agentIndex + 1) % num_agents
            next_depth = depth - 1 if next_agent == 0 else depth

            _, successor_value = self.alphaBeta(successor, next_depth, next_agent, alpha, beta)

            if is_pacman:
                if successor_value > best_value:
                    best_value, best_action = successor_value, action
                if best_value > beta:
                    break
                alpha = max(alpha, best_value)
            else:
                if successor_value < best_value:
                    best_value, best_action = successor_value, action
                if best_value < alpha:
                    break
                beta = min(beta, best_value)

            # if beta <= alpha:
            #     break
            
            # best_value += random.uniform(-0.5, 0.5) 
            
        return best_action, best_value
    
    # def _actionScore(self, gameState, action):
    #     """预计算动作得分用于排序"""
    #     successor = gameState.generateSuccessor(0, action)
    #     return self.evaluationFunction(successor)
    
    def rankActions(self, gameState, actions):
        """
        Rank actions based on their immediate evaluation function value.
        - Prefers moving toward food.
        - Avoids reversing direction to prevent oscillation.
        """
        pacman_pos = gameState.getPacmanPosition()
        food_list = gameState.getFood().asList()
        capsule_list = gameState.getCapsules()
        last_action = gameState.getPacmanState().configuration.direction

        ranked_actions = []
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            successor_pos = successor.getPacmanPosition()

            score = self.evaluationFunction(successor)
            # score = 0

            if capsule_list:
                closest_capsule_distance = min(
                    util.manhattanDistance(successor_pos, capsule) for capsule in capsule_list
                )
                score -= closest_capsule_distance*5
            
            if food_list:
                closest_food_distance = min(
                    util.manhattanDistance(successor_pos, food) for food in food_list
                )
                score -= closest_food_distance*5

            if last_action and action != last_action:
                score -= 3  # 让 Pac-Man 更倾向于继续前进，而不是突然变向
                
            if (last_action == Directions.NORTH and action == Directions.SOUTH) or \
               (last_action == Directions.SOUTH and action == Directions.NORTH) or \
               (last_action == Directions.EAST and action == Directions.WEST) or \
               (last_action == Directions.WEST and action == Directions.EAST):
                score -= 20
                
            if action == Directions.STOP:
                score -= 50
            
            ranked_actions.append((score, action))

        ranked_actions.sort(reverse=True, key=lambda x: x[0])

        return [action for _, action in ranked_actions]



        
# python pacman.py -l layouts/q2_trickyClassic.lay -p Q2_Agent --timeout=30