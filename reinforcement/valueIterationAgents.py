# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        i_iteration = 0
        while i_iteration < self.iterations: #we execute the number of iterations provided
          aux_values = util.Counter() # we need a variable to store the computed q values
          for s in self.mdp.getStates(): #for each state
            if not self.mdp.isTerminal(s): #we look if it's terminal
              possible_actions = self.mdp.getPossibleActions(s) #get all possible actions
              aux_values[s] = self.computeQValueFromValues(s, possible_actions[0]) #we assign the first action q value
              for a in possible_actions[1:]: #for each action left, we compute the q_val 
                q_val = self.computeQValueFromValues(s, a)
                if q_val > aux_values[s]: #if q val is bigger than actual value, we change it
                  aux_values[s] = q_val
            else:
              aux_values[s] = 0

          self.values = aux_values #actualize values with the new ones at the end of each iteration
          
          i_iteration += 1
      

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        #Q*(s,a)= SUM[Pa(new_s|s)[r(s,a)+d*V(new_s)]
        
        q_val = 0 #start q value at 0
        R = self.mdp.getReward #the reward function
        d = self.discount #the discount factor
        V = self.values #the calues dictionary

        all_posible_states_and_probs = self.mdp.getTransitionStatesAndProbs(state, action)
        for new_s, p in all_posible_states_and_probs:
          q_val += p * ( R(state, action, new_s) + d * V[new_s] ) #we calculate Pa(new_s|s)[r(s,a)+d*V(new_s)
        
        return q_val

        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state): #return None if state is terminal
          return None

        policies = [(self.computeQValueFromValues(state, action), action) for action in self.mdp.getPossibleActions(state)]
        
        return max(policies,key=lambda item:item[0])[1] 

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
