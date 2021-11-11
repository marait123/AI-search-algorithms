from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils

# TODO: Import any modules or write any helper functions you want to use


def log(message):
    with open("debug.txt", "a") as f:
        f.writelines([message])
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
    front_count = 1

    while front_count != 0:
        parent = fronteir.pop(0)
        front_count -= 1
        explored[parent] = True
        if(parent == initial_state):
            return ["I found solution"]
        reachable_actions = problem.get_actions(parent)
        for action in reachable_actions:
            child = problem.get_successor(parent, action)
            if child not in explored and child not in fronteir:
                fronteir.append(child)
                front_count += 1

    return None


def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    utils.NotImplemented()