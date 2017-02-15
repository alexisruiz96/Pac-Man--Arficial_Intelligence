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

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
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

    def evaluationFunction(self, currentGameState, action):
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
        man_score = 0
        penalization_die = 100
        collision_occurs = False
        max_man_dist = 1
        
        
        """
        for g in newGhostStates:
          man_dist = alpha*manhattanDistance(g.getPosition(), newPos)
          if man_score < max_man_dist:
            man_score += -100
        """
        #print("man score: "+str(man_score))
        score = successorGameState.getScore()
        #ideas to use with score
        #1. distance from ghost
        ghost_man_score = 0
        ghost_score_factor = 0
        for g in newGhostStates:
          ghost_man_score += max(3, ghost_score_factor*manhattanDistance(g.getPosition(), newPos))
        score += ghost_man_score
        #2. avoid collisions with ghosts
        #3. count food left
        #4. manhattan distance between closest food
        nearest_f = ""
        nearest_f_man_dist = float("Inf")
        x = 0
        y = 0
        for row in newFood:
          for f in row:
            if f:
              food_pos = (x, y)
              f_mand = manhattanDistance((x, y), newPos)
              #score -= f_mand
                #nearest_f_man_dist = f_mand
                #nearest_f = food_pos
          y += 1
        x += 1

        if action == Directions.STOP:
          score -= 300

        #current_f_man = manhattanDistance(nearest_f, currentGameState.getPacmanPosition())
        #print(current_f_man)
        #print(nearest_f_man_dist)
        #if current_f_man >= nearest_f_man_dist:
        #  score +=100

        #print(current_f_man)
        #print(nearest_f_man_dist)

        food_man_score = 0
        food_score_factor = 1
        
        #score -= food_score_factor
        #score = successorGameState.getScore() + man_score
        #5. if we have food, go:

        #if collision_occurs:
        #  score = score -penalization_die
        # 
        #print(score)
        return score

def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        "*** YOUR CODE HERE ***"
        def maxval(gameState, depth):
          depth += 1
          #base case, we look if we have win, lose or reached max depth
          if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
          v = float('-Inf')
          for a in gameState.getLegalActions(0): #get allowed pacman actions
            v = max(v, minval(gameState.generateSuccessor(0, a), depth, 1))
          return v

        def minval(gameState, depth, ghostIndex):
          if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

          v = float('Inf')
          for a in gameState.getLegalActions(ghostIndex): #get allowed pacman actions
            if ghostIndex == (gameState.getNumAgents()-1): #es el ultimo ghost
              v = min(v, maxval(gameState.generateSuccessor(ghostIndex, a), depth))
            else: #miramos a los otros ghost i escojemos el minimo valor
              v = min(v, minval(gameState.generateSuccessor(ghostIndex, a), depth, ghostIndex+1))
          return v

        vals_of_min =[]
        for a in gameState.getLegalActions(0):
          depth = 0
          vals_of_min.append((minval(gameState.generateSuccessor(0, a), depth, 1), a))

        return max(vals_of_min,key=lambda item:item[0])[1]
        
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def maxval(gameState, depth, alpha, beta):
          depth += 1
          #base case, we look if we have win, lose or reached max depth
          if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
          v = float('-Inf')
          for a in gameState.getLegalActions(0): #get allowed pacman actions
            v = max(v, minval(gameState.generateSuccessor(0, a), depth, 1, alpha, beta))
            if v > beta: #
              return v
            alpha = max(alpha, v) #we actualize alpha with max value between alpha and v
          return v

        def minval(gameState, depth, ghostIndex, alpha, beta):
          if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
          v = float('Inf')
          for a in gameState.getLegalActions(ghostIndex): #get allowed pacman actions
            if ghostIndex == (gameState.getNumAgents()-1): #es el ultimo ghost
              v = min(v, maxval(gameState.generateSuccessor(ghostIndex, a), depth, alpha, beta))
            else: #miramos a los otros ghost i escojemos el minimo valor
              v = min(v, minval(gameState.generateSuccessor(ghostIndex, a), depth, ghostIndex+1, alpha, beta))
            if v < alpha: # we prune, never will find a smallest v
              return v
            beta = min(beta, v) #we actualize beta with min value between beta and v
          return v

        
        alpha = float('-Inf')
        beta = float('Inf')
        vals_of_min =[]
        for a in gameState.getLegalActions(0):
          depth = 0
          vals_of_min.append((minval(gameState.generateSuccessor(0, a), depth, 1, alpha, beta), a))
          max_min_val = max(vals_of_min,key=lambda item:item[0])[0]
          max_minaction = max(vals_of_min,key=lambda item:item[0])[1]
          if max_min_val>beta:
            return max_minaction
          alpha = max(alpha, max_min_val)
          


        return max(vals_of_min,key=lambda item:item[0])[1]

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

