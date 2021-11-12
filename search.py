from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

# TODO: Import any modules or write any helper functions you want to use
import queue


def log(*message):
    with open("debug.txt", "a") as f:
        f.write(str(message) + "\n")
        f.close()


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
    class myCounter():
        def __init__(self):
            self.count = 0

        def get(self):
            self.count += 1
            return self.count
    counter = myCounter()

    explored = {}
    fronteir = queue.PriorityQueue()
    fronteir.put((0, counter.get(), initial_state))
    front_hash = {}
    front_hash[initial_state] = 0

    # this more optimized than using len(fronteir) as len traverses the list
    front_count = 1
    parent_graph = {}
    while front_count != 0:
        priority, _, parent = fronteir.get()
        front_count -= 1
        explored[parent] = True

        if problem.is_goal(parent):  # if goal is reached
            par, act = parent_graph[parent]
            actionList = []
            while par != initial_state:
                actionList.append(act)
                par, act = parent_graph[par]
            actionList.append(act)  # append the action from the initial state
            reactionList = [a for a in reversed(actionList)]
            return reactionList

        reachable_actions = problem.get_actions(parent)
        for action in reachable_actions:
            child = problem.get_successor(parent, action)
            if child not in explored and child not in front_hash:
                # insert child in fronteir
                parent_graph[child] = (parent, action)
                cost = front_hash[parent] + \
                    problem.get_cost(parent, action)
                fronteir.put((cost, counter.get(), child))
                # this is the cost of adding it
                front_hash[child] = front_hash[parent] + \
                    problem.get_cost(parent, action)
                front_count += 1
            elif child in front_hash and front_hash[child] != -1:
                cost = front_hash[parent] + \
                    problem.get_cost(parent, action)
                if(cost < front_hash[child]):
                    front_hash[child] = cost
                    # replace the one with m
                    fronteir.put((cost, counter.get(), initial_state))

                    pass
        front_hash[parent] = -1  # remove it from hash

    return None


def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # TODO: ADD YOUR CODE HERE
    utils.NotImplemented()
