import logging
import random

import util
from game import Actions, Agent, Directions
from logs.search_logger import log_function
from pacman import GameState
from util import manhattanDistance

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class Q2_Agent(Agent):
        
    def __init__(self, evalFn='scoreEvaluationFunction', depth='3'):
        self.index = 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        # self added
        # self.previous_positions = []
        # self.previous_actions = []
        # self.memory_length = 6  # 记忆长度设置为6，足够识别重复循环
        self.load_config()  # 加载参数

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

        best_action, best_value = self.alphaBeta(gameState, depth=2, agentIndex=0, alpha=-float('inf'), beta=float('inf'), evaluationFunction=self.betterEvaluation)
        # best_value, best_action = self.alphaBeta(gameState, self.depth, 0, float("-inf"), float("inf"))
        
        # 记录 Pacman 行为历史
        # self.previous_positions.append(gameState.getPacmanPosition())
        # self.previous_actions.append(best_action)
        # if len(self.previous_positions) > self.memory_length:
        #     self.previous_positions.pop(0)
        # if len(self.previous_actions) > self.memory_length:
        #     self.previous_actions.pop(0)
        
        return best_action


    def alphaBeta(self, gameState, depth, agentIndex, alpha, beta, evaluationFunction):
        """
        Alpha-Beta Pruning with Minimax.
        """
        # check depth & end of game
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return None, evaluationFunction(gameState)

        num_agents = gameState.getNumAgents()
        is_pacman = (agentIndex == 0)

        # best_action = None
        # best_value = -float('inf') if is_pacman else float('inf')

        actions = gameState.getLegalActions(agentIndex)
        if Directions.STOP in actions:
            actions.remove(Directions.STOP)  # 不考虑停止动作
        if not actions:
            return None, evaluationFunction(gameState)
        
        # 随机打乱行动顺序，避免相同分数导致上下循环    但是去掉后竟然变好了！！理论上应该不影响啊
        # 解释：排序是稳定排序 vs 非稳定排序

        # random.shuffle(actions)
        
        successor_cache = {}
        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            successor_cache[action] = successor
        
        # actions = sorted(
        #     actions,
        #     key=lambda a: evaluationFunction(successor_cache[a]),
        #     reverse=is_pacman  # Pacman 用 max，Ghost 用 min
        # )
        # action顺序很重要！
        # if is_pacman:
        #     actions = self.rankActions(gameState, actions)
            # pass
        # else:
        #     actions = sorted(actions, key=lambda a: evaluationFunction(gameState.generateSuccessor(agentIndex, a)))

        best_value = -float('inf') if is_pacman else float('inf')
        best_action = actions[0] # 默认选择第一个 action
        
        for action in actions:
            successor = successor_cache[action]

            next_agent = (agentIndex + 1) % num_agents
            next_depth = depth - 1 if next_agent == 0 else depth

            _, successor_value = self.alphaBeta(successor, next_depth, next_agent, alpha, beta, evaluationFunction)

            if is_pacman:
                # # 加一个立即吃 food / capsule 的奖励
                # if len(successor.getCapsules()) < len(gameState.getCapsules()):
                #     successor_value += 80

                # # 显式判断是否吃到 food
                # if len(successor.getFood().asList()) < len(gameState.getFood().asList()):
                #     successor_value += 50
                    
                # old_ghosts = gameState.getGhostStates()
                # new_ghosts = successor.getGhostStates()
                # for old, new in zip(old_ghosts, new_ghosts):
                #     if old.scaredTimer > 0 and new.scaredTimer == 0:
                #         successor_value += 80  # 吃掉可吃的 ghost
                    
                if successor.getScore() > gameState.getScore():
                    successor_value += self.immediate_reward
                elif gameState.getScore() - successor.getScore() > 10:
                    successor_value -= self.immediate_reward * 1000
                
                if successor_value > best_value:
                    best_value, best_action = successor_value, action
                if best_value > beta: # beta prune
                    break
                alpha = max(alpha, best_value)
            else:
                if successor_value < best_value:
                    best_value, best_action = successor_value, action
                if best_value < alpha: # alpha prune
                    break
                beta = min(beta, best_value)
            
        return best_action, best_value
    
    # def isOscillating(self, action):
    #     if len(self.previous_actions) < 2:
    #         return False
    #     # 上一动作是前一个的反方向并且和当前动作一样（如：右 左 右）
    #     if self.previous_actions[-1] == Actions.reverseDirection(self.previous_actions[-2]) and action == self.previous_actions[-2]:
    #         return True
        
        
    def betterEvaluation(self, gameState):
        pacmanPos = gameState.getPacmanPosition()
        foodGrid = gameState.getFood()
        food = gameState.getFood().asList()
        capsules = gameState.getCapsules()
        ghostStates = gameState.getGhostStates()
        # ghostPositions = [g.getPosition() for g in ghostStates]
        scaredTimes = [g.scaredTimer for g in ghostStates]
        # action = gameState.getPacmanState().configuration.direction
        walls = gameState.getWalls()
        # 
        score = self.evaluationFunction(gameState)
        
        if food:
            foodDist = findNearestTargetDistance(pacmanPos, foodGrid, walls)
            if foodDist is not None:
                score += self.food_weight / (foodDist + 1)
            # minFoodDist = min(util.manhattanDistance(pacmanPos, f) for f in food)
            # score += 100.0 / (minFoodDist + 1)

        if capsules:
            capsuleGrid = gameState.getWalls().copy()  # 新建空 Grid
            for (x, y) in capsules:
                capsuleGrid[x][y] = True
            capsuleDist = findNearestTargetDistance(pacmanPos, capsuleGrid, walls)
            # # 判断是否处于危险中
            # danger_nearby = any(
            #     getTrueDistance(pacmanPos, ghost.getPosition(), walls) <= 6
            #     for ghost, t in zip(ghostStates, scaredTimes) if t == 0
            # )

            # if capsuleDist is not None:
            #     if danger_nearby:
            #         score += 60.0 / (capsuleDist + 1)  # 鬼近就更想吃胶囊
            #     else:
            #         score += 50.0 / (capsuleDist + 1)   # 鬼远时稍微鼓励
                    
            if capsuleDist is not None:
                score += self.capsule_weight / (capsuleDist + 1)
            # minCapsuleDist = min(util.manhattanDistance(pacmanPos, c) for c in capsules)
            # score += 100.0 / (minCapsuleDist + 1)

        for ghost, timer in zip(ghostStates, scaredTimes):
            ghostPos = ghost.getPosition()

            # dist = util.manhattanDistance(pacmanPos, ghostPos)
            dist = getTrueDistance(pacmanPos, ghostPos, walls)
            if timer == 0:
                # Ghost 是危险的
                
                ghost_legal = Actions.getLegalNeighbors(ghostPos, gameState.getWalls())
                # if dist <= 2:
                #     if pacmanPos in ghost_legal:
                #         score -= 800  # 下一步可能撞脸
                #     else:
                #         score -= (3 - dist) * 200  # 超大惩罚（如 1格距 -160）
                if pacmanPos in ghost_legal:
                    score -= self.ghost_close_penalty * 2  # 可能下一步撞到 Pacman，惩罚
                # if dist < 2:
                #     score -= self.ghost_close_penalty # 距离太近，超大惩罚
                # elif dist < 5:
                #     score -= (6 - dist) ** 3
                # elif dist < 10:
                #     score -= (10 - dist) * 5
                elif dist < 5:
                    score -= (6 - dist) * 4
            else:
                # Ghost 是可吃的
                # if dist <= 5:
                #     score += 200.0 / (dist + 1)  # 吃白鬼奖励
                score += self.scared_ghost_reward / (dist + 1)
        
        # ✅ 震荡惩罚（关键）
        # 最近N步的位置如果重复，就扣分（尤其是形成循环）
        # recent_pos = self.previous_positions[-4:]  # 取最近4步
        # if recent_pos.count(pacmanPos) > 1:
        #     score -= 5  # 出现重复位置，说明震荡，扣分

        return score
    
    def load_config(self):
        # try:
        #     with open("agent_config.txt", "r") as f:
        #         content = f.read()
        #     kvs = dict(x.split("=") for x in content.strip().split("_"))
        #     self.food_weight = float(kvs.get("food_weight", 120))
        #     self.capsule_weight = float(kvs.get("capsule_weight", 100))
        #     self.ghost_close_penalty = float(kvs.get("ghost_close_penalty", 400))
        #     self.scared_ghost_reward = float(kvs.get("scared_ghost_reward", 350))
        #     self.immediate_reward = float(kvs.get("immediate_reward", 60))
        # except:
        self.food_weight = 110.24 # 120
        self.capsule_weight = 105.41 # 100
        self.ghost_close_penalty = 118.5 # 400
        self.scared_ghost_reward = 315.7 # 200
        self.immediate_reward = 40 # 60
        # self.food_weight = 120
        # self.capsule_weight = 100
        # self.ghost_close_penalty = 400
        # self.scared_ghost_reward = 200
        # self.immediate_reward = 60 # 60
        
def findNearestTargetDistance(startPos, targetGrid, walls):
    """
    BFS：返回从 startPos 到最近目标点的实际步数。
    targetGrid：可以是 foodGrid，也可以是 capsuleGrid
    """
    visited = set()
    queue = util.Queue()
    queue.push((startPos, 0))

    while not queue.isEmpty():
        pos, dist = queue.pop()
        if pos in visited:
            continue
        visited.add(pos)

        x, y = pos
        if targetGrid[x][y]:  # food / capsule
            return dist

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            next_x, next_y = x + dx, y + dy
            if not walls[next_x][next_y]:
                queue.push(((next_x, next_y), dist + 1))
    return None 

def getTrueDistance(startPos, endPos, walls):
    """
    用 BFS 计算 startPos 到 endPos 的最短路径距离，考虑墙体。
    """
    ghost_x, ghost_y = endPos
    endPos = (int(ghost_x), int(ghost_y))
    visited = set()
    queue = util.Queue()
    queue.push((startPos, 0))

    while not queue.isEmpty():
        pos, dist = queue.pop()
        if pos in visited:
            continue
        visited.add(pos)

        if pos == endPos:
            return dist

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            next_x, next_y = pos[0] + dx, pos[1] + dy
            if not walls[next_x][next_y]:
                queue.push(((next_x, next_y), dist + 1))
        
    print("Error: no path found!\n", startPos, endPos)
        
    return None  # 到不了

    # def rankActions(self, gameState, actions):
    #     pacman_pos = gameState.getPacmanPosition()
    #     food_list = gameState.getFood().asList()
    #     capsule_list = gameState.getCapsules()
    #     last_action = gameState.getPacmanState().configuration.direction

    #     ranked_actions = []
    #     for action in actions:
    #         successor = gameState.generateSuccessor(0, action)
    #         successor_pos = successor.getPacmanPosition()

    #         score = self.evaluationFunction(successor)

    #         if capsule_list:
    #             closest_capsule_distance = min(
    #                 util.manhattanDistance(successor_pos, capsule) for capsule in capsule_list)
    #             score -= closest_capsule_distance * 4

    #         if food_list:
    #             closest_food_distance = min(
    #                 util.manhattanDistance(successor_pos, food) for food in food_list)
    #             score -= closest_food_distance * 5

    #         # if last_action and action == last_action:
    #         #     score += 3

    #         # 反方向
    #         if last_action and action == Actions.reverseDirection(last_action):
    #             score -= 100

    #         # 走回头路
    #         # if successor_pos in self.previous_positions:
    #         #     score -= 5

    #         # 检测震荡行为
    #         # if self.isOscillating(action):
    #         #     score -= 30

    #         # 随机扰动避免评分一致
    #         score += random.uniform(-0.1, 0.1)

    #         ranked_actions.append((score, action))

    #     # 分数高优先，若分数相同，动作顺序固定避免抖动
    #     ranked_actions.sort(key=lambda x: (-x[0], x[1]))
    #     return [action for _, action in ranked_actions]

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

        
# python pacman.py -l layouts/q2_dangerClassic.lay -p Q2_Agent --timeout=30