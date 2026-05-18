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
        scared because of Pacman having eaten a power pellet.

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
        # Tính khoảng cách tới con ma gần nhất (chỉ xét ma không bị sợ)
        minGhostDist = float('inf')
        for ghostState in newGhostStates:
            # Chỉ né những con ma có scaredTimer == 0
            if ghostState.scaredTimer == 0:
                dist = manhattanDistance(newPos, ghostState.getPosition())
                minGhostDist = min(minGhostDist, dist)

        # Tính khoảng cách tới viên thức ăn gần nhất
        foodList = newFood.asList()
        minFoodDist = float('inf')
        for foodPos in foodList:
            dist = manhattanDistance(newPos, foodPos)
            minFoodDist = min(minFoodDist, dist)
        
        # Nếu không còn thức ăn, khoảng cách coi như bằng 0
        if not foodList:
            minFoodDist = 0

        # Công thức Evaluation nâng cấp:
        # 1. Sử dụng nghịch đảo của minFoodDist (1.0 / dist) để khuyến khích tiến lại gần thức ăn
        # 2. Trừng phạt nặng nếu minGhostDist quá nhỏ (ví dụ <= 1)
        
        score = successorGameState.getScore()
        
        # Thêm điểm thưởng dựa trên khoảng cách thức ăn (càng gần điểm càng cao)
        if minFoodDist > 0:
            score += 10.0 / minFoodDist
            
        # Trừ điểm nếu ma ở quá gần (né ma)
        if minGhostDist <= 1:
            score -= 500 # Phạt cực nặng nếu đứng cạnh ma
        else:
            score -= 2.0 / minGhostDist # Phạt nhẹ dựa trên khoảng cách ma
            
        return score
        # return successorGameState.getScore()

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
        score, action = self.minimaxSearch(gameState, 0, self.depth)
        return action
        util.raiseNotDefined()
    def minimaxSearch(self, gameState, agentIndex, depth):
        # Điều kiện dừng(Thắng, Thua, hoặc đã duyệt hết chiều sâu depth = 0)
        if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState), Directions.STOP
        if agentIndex == 0:
            return self.maximizer(gameState, agentIndex, depth)
        else:
            return self.minimizer(gameState, agentIndex, depth)
        
    def maximizer(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        # Nếu không có hành động nào hợp lệ
        if not actions:
            return self.evaluationFunction(gameState), Directions.STOP
        
        # Pacman (luôn là Agent 0) đi xong luôn chuyển sang Ghost 1(nếu có)
        # Giữ nguyên depth vì chưa xong 1 lượt (Ply)
        if agentIndex == gameState.getNumAgents() - 1: # Trường hợp không có ma
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = 1
            nextDepth = depth
        
        maxScore = float('-inf')
        maxAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            newScore = self.minimaxSearch(successor, nextAgent, nextDepth)[0]
            if newScore > maxScore:
                maxScore = newScore
                maxAction = action

        return maxScore, maxAction
    
    def minimizer(self, gameState, agentIndex, depth):
        actions = gameState.getLegalActions(agentIndex)
        # Nếu không có hành động nào hợp lệ
        if not actions:
            return self.evaluationFunction(gameState), Directions.STOP
        
        # xác định Agent tiếp theo, nếu là agent là ma cuối thì trả về pacman(agentIndex == 0)
        if agentIndex == gameState.getNumAgents() - 1:
            nextAgent = 0
            nextDepth = depth - 1
        else:
            nextAgent = agentIndex + 1
            nextDepth = depth
        
        minScore = float('inf')
        minAction = Directions.STOP

        for action in actions:
            successor = gameState.generateSuccessor(agentIndex, action)
            newScore = self.minimaxSearch(successor, nextAgent, nextDepth)[0]
            if newScore < minScore:
                minScore = newScore
                minAction = action

        return minScore, minAction


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
            return self.maximizer(gameState, agentIndex, depth, alpha, beta)
        else:
            return self.minimizer(gameState, agentIndex, depth, alpha, beta)
            
    def maximizer(self, gameState, agentIndex, depth, alpha, beta):
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
        
    def minimizer(self, gameState, agentIndex, depth, alpha, beta):
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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did> 
    It considers:
    - Distance to the nearest food: encourages Pacman to move toward food.
    - Distance to ghosts:
        + Penalizes being close to active (non-scared) ghosts.
        + Rewards approaching scared ghosts for potential points.
    - Remaining food count: penalized to encourage faster clearing.
    - Remaining capsules: slightly penalized to promote usage.
    - Current game score: included as a base metric.

    The function uses inverse distance (1 / (d + 1)) to create smooth
    gradients and avoid division by zero. When ghosts are scared,
    Pacman is encouraged to chase them instead of avoiding.

    Overall, the heuristic balances survival and efficiency, helping
    the agent perform well with shallow search depth (e.g., depth = 2).
    """
    "*** YOUR CODE HERE ***"
    pacman_pos = currentGameState.getPacmanPosition()
    foods = currentGameState.getFood().asList()
    ghost_states = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()
    score = currentGameState.getScore()

    if foods:
        min_food_dist = min([manhattanDistance(food, pacman_pos) for food in foods])
        score += 1.0 / min_food_dist 

    score -= 4 * len(foods)
    score -= 20 * len(capsules)

    active_ghost_dists = []
    scared_ghost_dists = []

    for ghost in ghost_states:
        dist = manhattanDistance(ghost.getPosition(), pacman_pos)
        if ghost.scaredTimer > 0:
            scared_ghost_dists.append(dist)
        else:
            active_ghost_dists.append(dist)

    if active_ghost_dists:
        min_active_dist = min(active_ghost_dists)
        if min_active_dist <= 1:
            return -999999 
        else:
            score -= 2.0 / min_active_dist 

    if scared_ghost_dists:
        min_scared_dist = min(scared_ghost_dists)
        score += 3.0 / (min_scared_dist + 1) 

    return score

# Abbreviation
better = betterEvaluationFunction
