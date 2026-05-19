# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power p ellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foods = newFood.asList()
        nearestGhostDis = 1e9
        for ghost_state in newGhostStates:
            ghost_x, ghost_y = ghost_state.getPosition()
            ghost_x = int(ghost_x)
            ghost_y = int(ghost_y)
            if ghost_state.scaredTimer == 0:
                nearestGhostDis = min(nearestGhostDis, manhattanDistance((ghost_x, ghost_y), newPos))
        nearestFoodDis = 1e9
        for food in foods:
            nearestFoodDis = min(nearestFoodDis, manhattanDistance(food, newPos))
        if not foods:
            nearestFoodDis = 0
        return successorGameState.getScore() - 7 / (nearestGhostDis + 1) - nearestFoodDis / 3


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

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

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        action = self.minimaxSearch(gameState, agentIndex=0, depth=self.depth)[1]
        return action
    

    def minimaxSearch(self, gameState, agentIndex, depth):
        if depth == 0 or gameState.isLose() or gameState.isWin():
            ret = self.evaluationFunction(gameState), Directions.STOP
        elif agentIndex == 0:
            ret = self.max_value(gameState, agentIndex, depth)
        else:
            ret = self.min_value(gameState, agentIndex, depth)
        return ret

    def min_value(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent, next_depth = 0, depth - 1
        else:
            next_agent, next_depth = agentIndex + 1, depth
        min_score = 1e9
        min_action = Directions.STOP
        for action in actions:
            successor_game_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.minimaxSearch(successor_game_state, next_agent, next_depth)[0]
            if new_score < min_score:
                min_score, min_action = new_score, action
        return min_score, min_action

    def max_value(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        if agentIndex == gameState.getNumAgents() - 1:
            next_agent, next_depth = 0, depth - 1
        else:
            next_agent, next_depth = agentIndex + 1, depth
        max_score = -1e9
        max_action = Directions.STOP
        for action in actions:
            successor_game_state = gameState.generateSuccessor(agentIndex, action)
            new_score = self.minimaxSearch(successor_game_state, next_agent, next_depth)[0]
            if new_score > max_score:
                max_score, max_action = new_score, action
        return max_score, max_action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Khởi tạo giá trị vô cực, rồi gán alpha là cực âm, beta là cực dương
        inf = float('inf')
        # Lấy kết quả hàm tìm kiếm, trả về hành động
        return self.alphaBetaSearch(gameState, 0, self.depth, -inf, inf)[1]
        # util.raiseNotDefined()

    def alphaBetaSearch(self, gameState, agentIndex, depth, alpha, beta):
        # Điều kiện dừng(Thắng, thua, hết độ sâu)
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), Directions.STOP
            
        if agentIndex == 0:
            return self.max_value(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.min_value(gameState, agentIndex, depth, alpha, beta)
            
    def max_value(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        if not actions:
            return self.evaluationFunction(gameState), Directions.STOP
            
        # Xác định Agent tiếp theo, nếu map chỉ không có ma thì agent giữ nguyên, depth giảm 1
        # Có ma thì tăng agentIndex, depth giữ
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth
            
        v = float("-inf")
        bestAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            # Lấy điểm dưới báo lên
            score = self.alphaBetaSearch(successor, nextAgent, nextDepth, alpha, beta)[0]

            if score > v:
                v = score
                bestAction = action

            if v > beta:
                return v, bestAction
                
            alpha = max(alpha, v)

        return v, bestAction
        
    def min_value(self, gameState, agentIndex, depth, alpha, beta):
        actions = gameState.getLegalActions(agentIndex)
        if not actions:
            return self.evaluationFunction(gameState), Directions.STOP
            
        # Xác định xem con sau có phải là ma cuối cùng hay không
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth
            
        v = float("inf")
        bestAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            score = self.alphaBetaSearch(successor, nextAgent, nextDepth, alpha, beta)[0]

            if score < v:
                v = score
                bestAction = action
                
            if v < alpha:
                return v, bestAction
                
            beta = min(beta, v)

        return v, bestAction
                
                
class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        # Gọi hàm expectimax từ agent đầu tiên (Pacman = 0)
        # với độ sâu tìm kiếm đã cho
        return self.expectimaxsearch(gameState, 0, self.depth)[1]

    def expectimaxsearch(self, game_state, agent_index, depth):

        # Điều kiện dừng:
        # - Độ sâu = 0
        # - Pacman thắng
        # - Pacman thua
        if depth == 0 or game_state.isWin() or game_state.isLose():

            # Trả về điểm đánh giá của trạng thái hiện tại
            # và action STOP
            ret = self.evaluationFunction(game_state), Directions.STOP

        # Nếu là lượt của Pacman
        elif agent_index == 0:

            # Dùng hàm maximizer để chọn nước đi tốt nhất
            ret = self.max_value(game_state, agent_index, depth)

        # Nếu là lượt của Ghost
        else:

            # Tính giá trị kỳ vọng (Expectation)
            ret = self.expectation(game_state, agent_index, depth)

        return ret


    def max_value(self, game_state, agent_index, depth):

        # Lấy tất cả hành động hợp lệ của Pacman
        actions = game_state.getLegalActions(agent_index)

        # Kiểm tra agent tiếp theo
        if agent_index == game_state.getNumAgents() - 1:

            # Nếu agent hiện tại là agent cuối cùng
            # quay lại Pacman và giảm depth
            next_agent, next_depth = 0, depth - 1

        else:

            # Chuyển sang agent tiếp theo
            next_agent, next_depth = agent_index + 1, depth

        # Khởi tạo điểm lớn nhất rất nhỏ
        max_score, max_action = -1e9, Directions.STOP

        # Duyệt qua từng action
        for action in actions:

            # Sinh trạng thái kế tiếp
            successor_game_state = game_state.generateSuccessor(
                agent_index,
                action
            )

            # Gọi đệ quy để tính điểm
            new_score = self.expectimaxsearch(
                successor_game_state,
                next_agent,
                next_depth
            )[0]

            # Nếu tìm được điểm tốt hơn
            if new_score > max_score:

                # Cập nhật điểm và action tốt nhất
                max_score, max_action = new_score, action

        return max_score, max_action


    def expectation(self, game_state, agent_index, depth):

        # Lấy các hành động hợp lệ của Ghost
        actions = game_state.getLegalActions(agent_index)

        # Xác định agent kế tiếp
        if agent_index == game_state.getNumAgents() - 1:

            # Nếu là agent cuối cùng
            # quay lại Pacman và giảm depth
            next_agent, next_depth = 0, depth - 1

        else:

            # Sang agent tiếp theo
            next_agent, next_depth = agent_index + 1, depth

        # Tổng giá trị kỳ vọng
        exp_score = 0

        # Ghost không cần action tối ưu
        exp_action = Directions.STOP

        # Duyệt tất cả action
        for action in actions:

            # Sinh trạng thái kế tiếp
            successor_game_state = game_state.generateSuccessor(
                agent_index,
                action
            )

            # Cộng điểm từ các trạng thái con
            exp_score += self.expectimaxsearch(
                successor_game_state,
                next_agent,
                next_depth
            )[0]

        # Vì ghost chọn random đều nhau
        # nên lấy trung bình cộng
        exp_score /= len(actions)

        # exp_action không dùng tới
        return exp_score, exp_action

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).
    """

    pacman_pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    ghost_states = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    # Start from the real game score so eating is always rewarded
    score = currentGameState.getScore()

    # Food proximity
    # Reward being close to the nearest food; closer = higher bonus
    if foods:
        min_food_dist = min(manhattanDistance(food, pacman_pos) for food in foods)
        score += 1.0 / min_food_dist  # No +1 needed; foods are never at distance 0

    # Penalize number of remaining food pellets to incentivize fast clearing
    score -= 4 * len(foods)

    # Penalize uneaten capsules to encourage Pacman to use power pellets
    score -= 20 * len(capsules)

    # Ghost classification
    # Separate ghosts into dangerous (active) and huntable (scared)
    active_ghost_dists = []
    scared_ghost_dists = []

    for ghost in ghost_states:
        dist = manhattanDistance(ghost.getPosition(), pacman_pos)
        if ghost.scaredTimer > 0:
            scared_ghost_dists.append(dist)
        else:
            active_ghost_dists.append(dist)

    # Active ghost penalty
    if active_ghost_dists:
        min_active_dist = min(active_ghost_dists)
        if min_active_dist <= 1:
            # Immediate death risk — treat this state as catastrophic
            return -999999
        else:
            # Smooth penalty: grows as Pacman gets closer to a dangerous ghost
            score -= 2.0 / min_active_dist

    # Scared ghost reward
    # When ghosts are scared, flip strategy: chase instead of flee
    if scared_ghost_dists:
        min_scared_dist = min(scared_ghost_dists)
        score += 3.0 / (min_scared_dist + 1)  # +1 guards against dist == 0

    return score

# Abbreviation
better = betterEvaluationFunction
