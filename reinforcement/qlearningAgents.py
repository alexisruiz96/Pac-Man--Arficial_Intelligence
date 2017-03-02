# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.qvalues = util.Counter() #for every state and action we store his qvalue
    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        key = (state,action)

        if key not in self.qvalues:#if key is not in qvalues we initialize in 0
          self.qvalues[key] = 0.0
        
        return self.qvalues[key]

          
        util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        temp = util.Counter() #temporal counter that counts for a set of given keys
        legalActions = self.getLegalActions(state)
        if len(legalActions) == 0: #there are no legal actions
          bestActionVal = 0.0
          return bestActionVal

        for action in legalActions: #for every action save qvalue
          temp[action] = self.getQValue(state,action)
        #temp.argMax() returns key with highest value 
        bestActionVal = temp[temp.argMax()]#returns value of action with highest value
        return bestActionVal
        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        legalActions = self.getLegalActions(state)
        temp = util.Counter() #temporal counter that counts for a set of given keys
        maxList = util.Counter()
        bestActionVal = 0.0
        bestAction = None
        if len(legalActions) == 0: #fi there is not a legal actions we return None
          return None

        for action in legalActions: #for every action inside legalActions we get the qValue and store it in his position
          temp[action] = self.getQValue(state,action)
        '''
        DON'T WORK
        for action in temp.sortedKeys(): #to break ties
          print action
          #print temp[action]
          if temp[action] == bestActionVal:
            maxList.append(action) 
          if temp[action] != bestActionVal:
            break 
        print maxList[0]
        bestAction = random.choice(maxList)
        '''
        
        return temp.argMax()
        util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        if len(legalActions)==0:#when there are no legal actions
          return None

        if util.flipCoin(self.epsilon):#chooses random actions an epsilon fraction of the time
          action = random.choice(legalActions) 
        else:
          action = self.getPolicy(state)#apply policy to an action given a state

        return action
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        #Q(s,a) = (1-alpha)*Q(s,a) + alpha*[r(s,a) + gamma * maxQ(s',a)]
        alpha = self.alpha
        gamma = self.discount
        oldValue = self.getQValue(state,action)
        newValue = self.computeValueFromQValues(nextState)
        self.qvalues[(state,action)] = (1-alpha)*oldValue + alpha * (reward + gamma * newValue)
        #update the qvalue given a state and an action

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        #Q-function
        #Q(s,a)=sum(fi(s,a)wi)
        "*** YOUR CODE HERE ***"
        q = 0 #initialize q to 0
        weights = self.getWeights() #weight vector
        features = self.featExtractor.getFeatures(state,action)#returns a dict from features to counts
        
        for f in features:#for every feature we calculate his value witg Q-function
          q+=weights[f]*features[f]
        return q

        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        weights = self.getWeights()
        features = self.featExtractor.getFeatures(state,action)
        alpha = self.alpha
        gamma = self.discount
        difference = (reward + gamma * self.computeValueFromQValues(nextState)) - self.getQValue(state,action)
        for f in features:#for every feature we update the weight associated to it
          weights[f] = weights[f] + alpha * difference * features[f]#calculate updated weight value
        

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
