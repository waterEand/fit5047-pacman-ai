import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance

import math


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
        # self.temperature = 1.0
        self.previous_positions = []  # 用于防止走回头路
        self.previous_actions = []    # 用于检测震荡行为
        self.memory_length = 4        # 记忆长度
        
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

        # self.temperature -= 0.005
        # if self.temperature < 0.01:
        #     self.temperature = 0.01
        best_action, best_value = self.alphaBeta(gameState, depth=self.depth, agentIndex=0, alpha=-float('inf'), beta=float('inf'))
        # best_value, best_action = self.alphaBeta(gameState, self.depth, 0, float("-inf"), float("inf"))
        
        successor = gameState.generateSuccessor(0, best_action)
        pos = successor.getPacmanPosition()

        self.previous_positions.append(pos)
        self.previous_actions.append(best_action)

        if len(self.previous_positions) > self.memory_length:
            self.previous_positions.pop(0)
        if len(self.previous_actions) > self.memory_length:
            self.previous_actions.pop(0)

        return best_action


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
        random.shuffle(actions)
        # action顺序很重要！
        if is_pacman:
            # actions = sorted(
            #     actions, 
            #     key=lambda action: self.evaluationFunction(gameState.generateSuccessor(agentIndex, action)),
            #     # key=lambda a: (self._actionScore(gameState, a), a), 
            #     reverse=True
            # )
            actions = self.rankActions(gameState, actions)
            # pass
        # else:
            # random.shuffle(actions)
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
                    # if action == Directions.STOP:
                    #     x = (self.temperature - 0.5) * 12
                    #     s = 1 / (1 + math.exp(-x))
                    #     reduce_amount = s * 0.9 + 0.1
                    #     successor_value *= reduce_amount
                    #     if successor_value > best_value:
                    #         best_value, best_action = successor_value, action
                    # else:
                    #     best_value, best_action = successor_value, action
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
            
        return best_action, best_value
    
    def isOscillating(self, action):
        if len(self.previous_actions) < 2:
            return False
        # 上一动作是前一个的反方向并且和当前动作一样（如：右 左 右）
        return (self.previous_actions[-1] == Actions.reverseDirection(self.previous_actions[-2]) and
                action == self.previous_actions[-2])
    
    def rankActions(self, gameState, actions):
        pacman_pos = gameState.getPacmanPosition()
        food_list = gameState.getFood().asList()
        capsule_list = gameState.getCapsules()
        last_action = gameState.getPacmanState().configuration.direction

        ranked_actions = []
        for action in actions:
            successor = gameState.generateSuccessor(0, action)
            successor_pos = successor.getPacmanPosition()

            score = self.evaluationFunction(successor)

            if capsule_list:
                closest_capsule_distance = min(
                    util.manhattanDistance(successor_pos, capsule) for capsule in capsule_list)
                score -= closest_capsule_distance * 4

            if food_list:
                closest_food_distance = min(
                    util.manhattanDistance(successor_pos, food) for food in food_list)
                score -= closest_food_distance * 5

            if action == Directions.STOP:
                score -= 100

            # if last_action and action == last_action:
            #     score += 3

            # 反方向
            if last_action and action == Actions.reverseDirection(last_action):
                score -= 10

            # 走回头路
            # if successor_pos in self.previous_positions:
            #     score -= 10

            # 检测震荡行为
            if self.isOscillating(action):
                score -= 30

            # 随机扰动避免评分一致
            score += random.uniform(-0.1, 0.1)

            ranked_actions.append((score, action))

        # 分数高优先，若分数相同，动作顺序固定避免抖动
        ranked_actions.sort(key=lambda x: (-x[0], x[1]))
        return [action for _, action in ranked_actions]
    
#     def rankActions(self, gameState, actions):
#         """
#         Rank actions based on their immediate evaluation function value.
#         - Prefers moving toward food.
#         - Avoids reversing direction to prevent oscillation.
#         """
#         pacman_pos = gameState.getPacmanPosition()
#         food_list = gameState.getFood().asList()
#         capsule_list = gameState.getCapsules()
#         last_action = gameState.getPacmanState().configuration.direction

#         ranked_actions = []
#         for action in actions:
#             successor = gameState.generateSuccessor(0, action)
#             successor_pos = successor.getPacmanPosition()

#             score = self.evaluationFunction(successor)
#             # score = 0

#             if capsule_list:
#                 closest_capsule_distance = min(
#                     util.manhattanDistance(successor_pos, capsule) for capsule in capsule_list
#                 )
#                 score -= closest_capsule_distance
            
#             if food_list:
#                 closest_food_distance = min(
#                     util.manhattanDistance(successor_pos, food) for food in food_list
#                 )
#                 score -= closest_food_distance*5

#             if last_action and action != last_action:
#                 score -= 1  # 让 Pac-Man 更倾向于继续前进，而不是突然变向
                
#             if (last_action == Directions.NORTH and action == Directions.SOUTH) or \
#                (last_action == Directions.SOUTH and action == Directions.NORTH) or \
#                (last_action == Directions.EAST and action == Directions.WEST) or \
#                (last_action == Directions.WEST and action == Directions.EAST):
#                 score -= 5
                
#             if action == Directions.STOP:
#                 score -= 20
            
#             ranked_actions.append((score, action))

#         # ranked_actions.sort(reverse=True, key=lambda x: x[0])
#         ranked_actions.sort(key=lambda x: (-x[0], x[1]))


#         return [action for _, action in ranked_actions]

        
# python pacman.py -l layouts/q2_originalClassic.lay -p Q2_Agent --timeout=30