from typing import Container, Tuple, Union
from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

# TODO: Import any modules or write any helper functions you want to use
import queue


def log(*message):
    with open("debug.txt", "a") as f:
        f.write(str(message) + "\n")
        f.close()


class MyQueue():
    def __init__(self):
        self.container = {}
        self.size = 0

    def len(self):
        return self.size

    def insert(self, key, costDic):
        """
        @params
        ------------------------------------------
        key : is the key used to store the costDic
        costDic: this is a dictionary of the shape {'cost':3.4, <extra>:...}
        """
        if key in self.container:
            if costDic['cost'] < self.container[key]['cost']:
                self.container[key] = costDic
            # else don't append
        else:
            self.container[key] = costDic
            self.size += 1

    def getValue(self, key):
        return self.container[key]

    def getCost(self, key):
        return self.container[key]['cost']

    def replace(self, key, new_costDic):
        self.container[key] = new_costDic

    def find(self, key) -> bool:
        return key in self.container

    def pop(self) -> Tuple[S, float]:
        minKey = min(self.container,
                     key=lambda key: self.container[key]['cost'])
        costDic = self.container[minKey]
        self.removeElement(minKey)
        return minKey, costDic

    def removeElement(self, key):
        self.size -= 1
        del self.container[key]

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution


def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    explored = {}
    fronteir = [initial_state]
    # this more optimized than using len(fronteir) as len traverses the list
    front_count = 1
    parent_graph = {}
    while front_count != 0:
        parent = fronteir.pop(0)
        front_count -= 1
        explored[parent] = True
        if problem.is_goal(parent):
            par, act = parent_graph[parent]
            # print("debugging1\n")
            # print("I found solution\n")
            # print("graph is ", parent_graph)
            # print("initial par and act ", par, "-", act)
            actionList = []
            while par != initial_state:
                # print("par and act ", par, "-", act)

                actionList.append(act)
                par, act = parent_graph[par]
            actionList.append(act)  # append the action from the initial state
            reactionList = [a for a in reversed(actionList)]
            return reactionList
        reachable_actions = problem.get_actions(parent)
        for action in reachable_actions:
            child = problem.get_successor(parent, action)
            if child not in explored and child not in fronteir:
                parent_graph[child] = (parent, action)
                fronteir.append(child)
                front_count += 1

    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # print("checking goal")
    def RecurDepth(i_state, explored):
        explored[i_state] = True
        if(problem.is_goal(i_state)):
            # print("goal is found")
            return []

        reachable_actions = problem.get_actions(i_state)
        for action in reachable_actions:
            child = problem.get_successor(i_state, action)
            if child not in explored:   # explore only unexplored nodes as this is graph search
                answer = RecurDepth(child, explored)
                if not(answer is None):
                    # the answer is formed so that near goal (answer) comes last in the list
                    return [action] + answer
        return None
    explored = {}
    return RecurDepth(initial_state, explored)


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # TODO: ADD YOUR CODE HERE
    fronteir = MyQueue()
    explored = {}
    fronteir.insert(initial_state, {'cost': 0})

    parent_graph = {}  # child will refer to his parent and the action
    # loop while fronteir not empty
    while fronteir.len() > 0:
        # get the 1st element in fronteir
        # print("fronteir.container ", fronteir.container)
        parentNode, parentDic = fronteir.pop()
        parentCost = parentDic['cost']
        # check if parentNode is the goal
        if problem.is_goal(parentNode):
            par, act = parent_graph[parentNode]
            actionList = []
            while par != initial_state:
                # print("par and act ", par, "-", act)
                actionList.append(act)
                par, act = parent_graph[par]
            actionList.append(act)  # append the action from the initial state
            reactionList = [a for a in reversed(actionList)]
            return reactionList
        # add parentNode to explored
        explored[parentNode] = True
        # loop on all possible actions
        for action in problem.get_actions(parentNode):
            childNode = problem.get_successor(parentNode, action)
            # calculate the newChild Cost
            childCost = parentCost + problem.get_cost(parentNode, action)
            # print("childCost is ", childCost)
            # childNode not in explored or fronteir
            if childNode not in explored and (not fronteir.find(childNode)):
                parent_graph[childNode] = (parentNode, action)
                fronteir.insert(childNode, {'cost': childCost})
            elif fronteir.find(childNode) and childCost < fronteir.getCost(childNode):
                parent_graph[childNode] = (parentNode, action)
                fronteir.replace(childNode, {'cost': childCost})
    return None


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    # def heuristic(dummy, dumb):
    #     return 0
    fronteir = MyQueue()
    explored = {}
    fronteir.insert(
        initial_state, {'cost': 0 + heuristic(problem, initial_state), 'gCost': 0})

    # print("initial is ", heuristic(problem, initial_state))
    parent_graph = {}  # child will refer to his parent and the action
    # loop while fronteir not empty
    while fronteir.len() > 0:
        # get the 1st element in fronteir
        # print("fronteir.container ", fronteir.container)
        parentNode, costDic = fronteir.pop()
        # this is the total heuristics + path cost
        parentCost = costDic['cost']
        parentGCost = costDic['gCost']  # this is the cumulative path Cost
        # check if parentNode is the goal
        if problem.is_goal(parentNode):
            # use backtracking on the parentGraph where a child refers to its parent
            par, act = parent_graph[parentNode]
            actionList = []
            while par != initial_state:
                # print("par and act ", par, "-", act)
                actionList.append(act)
                par, act = parent_graph[par]
            actionList.append(act)  # append the action from the initial state
            reactionList = [a for a in reversed(actionList)]
            return reactionList
        # add parentNode to explored
        explored[parentNode] = True
        # print("parentNode is ", parentNode, " parentCost is ", parentCost)

        # loop on all possible actions
        for action in problem.get_actions(parentNode):
            childNode = problem.get_successor(parentNode, action)
            # calculate the newChild Cost
            # child Cost is the cost from start to child + heuristic
            # adding the total parent cost directly is errornous
            childCost = parentGCost + \
                problem.get_cost(parentNode, action) + \
                heuristic(problem, childNode)
            childGCost = parentGCost + problem.get_cost(parentNode, action)

            if childNode not in explored and (not fronteir.find(childNode)):
                parent_graph[childNode] = (parentNode, action)
                fronteir.insert(
                    childNode, {'cost': childCost, 'gCost': childGCost})
            elif fronteir.find(childNode) and childCost < fronteir.getCost(childNode):
                parent_graph[childNode] = (parentNode, action)
                fronteir.replace(
                    childNode,  {'cost': childCost, 'gCost': childGCost})

    return None


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    fronteir = MyQueue()
    explored = {}
    fronteir.insert(initial_state, {'cost': heuristic(problem, initial_state)})
    parent_graph = {}  # child will refer to his parent and the action
    # loop while fronteir not empty
    while fronteir.len() > 0:
        # get the 1st element in fronteir
        parentNode, costDic = fronteir.pop()
        parent_cost = costDic['cost']
        # check if parentNode is the goal
        if problem.is_goal(parentNode):
            par, act = parent_graph[parentNode]
            actionList = []
            while par != initial_state:
                actionList.append(act)
                par, act = parent_graph[par]
            actionList.append(act)  # append the action from the initial state
            reactionList = [a for a in reversed(actionList)]
            return reactionList
        # add parentNode to explored
        explored[parentNode] = True
        # print("parentNode is ", parentNode, " parentCost is ", parentCost)

        # loop on all possible actions
        for action in problem.get_actions(parentNode):
            childNode = problem.get_successor(parentNode, action)
            # calculate the newChild Cost
            childCost = heuristic(problem, childNode)

            # childNode not in explored or fronteir
            if childNode not in explored and (not fronteir.find(childNode)):
                parent_graph[childNode] = (parentNode, action)
                fronteir.insert(childNode, {'cost': childCost})
            elif fronteir.find(childNode) and childCost < fronteir.getCost(childNode):
                parent_graph[childNode] = (parentNode, action)
                fronteir.replace(childNode, {'cost': childCost})

    return None
