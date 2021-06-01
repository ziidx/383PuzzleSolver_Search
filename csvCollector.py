# George Chiang
# Jack DeGuglielmo 30900481
# Homework 1: 8-puzzle Problem
# 9/18/2020
# Example run: `python solver.py bfs 802356174`
import time

from puzz import *
from pdqpq import *
import sys


class Node:
    def __init__(self, state, parent, move):
        self.state = state      # 8 puzzle obj
        self.parent = parent    # parent node
        self.move = move
        self.cost = 0

    def __hash__(self):
        return hash("".join(self.state._board))

    def __eq__(self, other):
        return "".join(self.state._board) == "".join(other.state._board)


def mod_heuristic(inputPuzzle):  # Modified misplaced manhattan distance function for Greedy B-F and A*
    """input puzzle as 2D List/Array
        1 = [0][1]
        2 = [0][2]
        3 = [1][0]
        4 = [1][1]
        5 = [1][2]
        6 = [2][0]
        7 = [2][1]
        8 = [2][2]
        Distance of tile x = x^2 * distance of x from its correct location
        totalManhattan += Manhattan distance of each tile
    """

    totalManhattan = 0
    distance = 0
    boardArr = [inputPuzzle._board[x:x + 3] for x in
                range(0, len(inputPuzzle._board), 3)]  # splits input puzzle into a 2d matrix board

    for i in range(1, 9):
        for x, lst in enumerate(boardArr):
            if str(i) in lst:
                numCoord = (x, lst.index(str(i)))
                if i == 1:
                    distance = numCoord[0] + abs(numCoord[1] - 1)
                    totalManhattan += distance
                if i == 2:
                    distance = numCoord[0] + abs(numCoord[1] - 2)
                    if isNoWeight is False:
                        totalManhattan += 4 * distance
                    else:
                        totalManhattan += distance
                if i == 3:
                    distance = abs(numCoord[0] - 1) + numCoord[1]
                    if isNoWeight is False:
                        totalManhattan += 9 * distance
                    else:
                        totalManhattan += distance
                if i == 4:
                    distance = abs(numCoord[0] - 1) + abs(numCoord[1] - 1)
                    if isNoWeight is False:
                        totalManhattan += 16 * distance
                    else:
                        totalManhattan += distance
                if i == 5:
                    distance = abs(numCoord[0] - 1) + abs(numCoord[1] - 2)
                    if isNoWeight is False:
                        totalManhattan += 25 * distance
                    else:
                        totalManhattan += distance
                if i == 6:
                    distance = abs(numCoord[0] - 2) + numCoord[1]
                    if isNoWeight is False:
                        totalManhattan += 36 * distance
                    else:
                        totalManhattan += distance
                if i == 7:
                    distance = abs(numCoord[0] - 2) + abs(numCoord[1] - 1)
                    if isNoWeight is False:
                        totalManhattan += 49 * distance
                    else:
                        totalManhattan += distance
                if i == 8:
                    distance = abs(numCoord[0] - 2) + abs(numCoord[1] - 2)
                    if isNoWeight is False:
                        totalManhattan += 64 * distance
                    else:
                        totalManhattan += distance
    return totalManhattan


def is_goal(inputPuzzle):
    goal = '012345678'
    if inputPuzzle.__str__() == goal:
        return True
    return False


def printSolution(solution, cost, frontier, expanded):
    counter = 0
    # for i in range(len(solution)):
    #     # print(i)
    #     print(str(counter) + "\t" + solution[i].move + "\t" + str(solution[i].state))
    #     counter += 1
    # print("path cost: ", cost)  # Haven't gotten to these yet (may need to move all this up to algo functions)
    # print("frontier: ", frontier)
    # print("expanded: ", expanded)

    print(cost,',', frontier,',', expanded)


def bfs(inputPuzzle):
    # print(inputPuzzle.pretty())
    solution = []
    totalCost = 0
    frontier = PriorityQueue()
    explored = set()
    startNode = Node(inputPuzzle, None, "start")  # Root parent is none
    solution.append(startNode)
    frontier.add(startNode)
    expandCount = 0
    frontierCount = 1
    if is_goal(inputPuzzle):
        printSolution(solution, 0, frontierCount, expandCount)
        return 1
    while frontier.empty() != True:  # while frontier is not empty
        node = frontier.pop()
        # print(node.state)
        explored.add(node)
        blankLoc = node.state.find('0')
        # print(blankLoc)
        succ = node.state.successors()
        expandCount += 1
        if expandCount >= 100000:
            print("Search halted")
            return printSolution(solution, totalCost, frontierCount, expandCount)

        for key in succ:
            # print(key)
            n = Node(succ[key], node, key)
            # print(isNoWeight)
            if isNoWeight:
                n.cost = 1
            else:
                n.cost = int(n.state._get_tile(blankLoc[0], blankLoc[1])) ** 2
            if (n not in frontier) and (n not in explored):
                # solution.append([key, n])
                # print(n.state)
                if is_goal(n.state):
                    # print("We found solution")
                    tmpNode = n
                    while tmpNode.parent is not None:
                        totalCost += tmpNode.cost
                        solution.insert(1, tmpNode)
                        tmpNode = tmpNode.parent
                    # solution.append(startNode)
                    return printSolution(solution, totalCost, frontierCount, expandCount)

                else:
                    frontier.add(n)
                    frontierCount += 1


def ucost(inputPuzzle):
    # print(inputPuzzle.pretty())
    solution = []
    frontier = PriorityQueue()
    explored = set()
    startNode = Node(inputPuzzle, None, "start")  # Root parent is none
    solution.append(startNode)
    frontier.add(startNode, 0)
    expandCount = 0
    frontierCount = 1
    if is_goal(inputPuzzle):
        return printSolution(solution, 0, frontierCount, expandCount)
    while not frontier.empty():
        node = frontier.pop()
        # print(node.state)
        if is_goal(node.state):
            tmpNode = node
            while tmpNode.parent is not None:
                # print(tmpNode.state)
                solution.insert(1, tmpNode)
                tmpNode = tmpNode.parent
            # solution.append(node)
            return printSolution(solution, node.cost, frontierCount, expandCount)
        explored.add(node)
        blankLoc = node.state.find('0')
        succ = node.state.successors()
        expandCount += 1
        if expandCount >= 100000:
            print("Search halted")
            return printSolution(solution, node.cost, frontierCount, expandCount)
        for key in succ:
            # print(key)
            n = Node(succ[key], node, key)
            if isNoWeight:
                n.cost = 1 + n.parent.cost
            else:
                n.cost = (int(n.state._get_tile(blankLoc[0], blankLoc[1])) ** 2) + n.parent.cost
            if (n not in frontier) and (n not in explored):
                frontier.add(n, n.cost)
                frontierCount += 1
            elif n in frontier and frontier.get(n) > n.cost:        # if we reach a repeat node
                frontier.add(n, n.cost)

    pass  # throw error


def greedy(inputPuzzle):
    # print(inputPuzzle.pretty())
    solution = []
    frontier = PriorityQueue()
    explored = set()
    startNode = Node(inputPuzzle, None, "start")  # Root parent is none
    solution.append(startNode)
    frontier.add(startNode, 0)
    expandCount = 0
    frontierCount = 1
    if is_goal(inputPuzzle):
        return printSolution(solution, 0, frontierCount, expandCount)
    while not frontier.empty():
        node = frontier.pop()
        # print(node.state)
        if is_goal(node.state):
            tmpNode = node
            while tmpNode.parent is not None:
                # print(tmpNode.state)
                solution.insert(1, tmpNode)
                tmpNode = tmpNode.parent
            # solution.append(node)
            return printSolution(solution, node.cost, frontierCount, expandCount)
        explored.add(node)
        blankLoc = node.state.find('0')
        succ = node.state.successors()
        expandCount += 1
        if expandCount >= 100000:
            # print("Search halted")
            return printSolution(solution, node.cost, frontierCount, expandCount)
        for key in succ:
            # print(key)
            n = Node(succ[key], node, key)
            if isNoWeight is False:
                n.cost = (int(n.state._get_tile(blankLoc[0], blankLoc[1])) ** 2) + n.parent.cost
            else:
                n.cost = 1 + n.parent.cost
            if (n not in frontier) and (n not in explored):
                frontier.add(n, mod_heuristic(n.state))
                # print(n.state)
                frontierCount += 1
    pass  # throw error



def astar(inputPuzzle):
    # print(inputPuzzle.pretty())
    solution = []
    frontier = PriorityQueue()
    explored = set()
    startNode = Node(inputPuzzle, None, "start")  # Root parent is none
    solution.append(startNode)
    frontier.add(startNode, 0)
    expandCount = 0
    frontierCount = 1
    if is_goal(inputPuzzle):
        return printSolution(solution, 0, frontierCount, expandCount)
    while not frontier.empty():
        node = frontier.pop()
        # print(node.state)
        if is_goal(node.state):
            tmpNode = node
            while tmpNode.parent is not None:
                # print(tmpNode.state)
                solution.insert(1, tmpNode)
                tmpNode = tmpNode.parent
            # solution.append(node)
            return printSolution(solution, node.cost, frontierCount, expandCount)
        explored.add(node)
        blankLoc = node.state.find('0')
        succ = node.state.successors()
        expandCount += 1
        if expandCount >= 100000:
            # print("Search halted")
            return printSolution(solution, node.cost, frontierCount, expandCount)
        for key in succ:
            # print(key)
            n = Node(succ[key], node, key)
            if isNoWeight is False:
                n.cost = (int(n.state._get_tile(blankLoc[0], blankLoc[1])) ** 2) + n.parent.cost
            else:
                n.cost = 1 + n.parent.cost
            if (n not in frontier) and (n not in explored):
                frontier.add(n, mod_heuristic(n.state) + n.cost)
                # print(n.state)
                frontierCount += 1
    pass  # throw error
    pass  # throw error


def main():

    # isBfs = False
    # isUcost = False
    # isGreedy = False
    # isAstar = False
    global isNoWeight
    isNoWeight = False
    # if sys.argv[1] == "bfs":
    #     isBfs = True
    # elif sys.argv[1] == "ucost":
    #     isUcost = True
    # elif sys.argv[1] == "greedy":
    #     isGreedy = True
    # elif sys.argv[1] == "astar":
    #     isAstar = True
    # else:
    #     print("Search type is not recognized.")
    #     return -1
    #
    # if len(sys.argv[2]) != 9:
    #     print("Starting board string is not recognized")
    #     return -1
    #
    # if len(sys.argv) > 3:
    #     if sys.argv[3] == "--noweight":
    #         isNoWeight = True
    #
    # startPuzzle = EightPuzzleBoard(sys.argv[2])
    #
    # if isBfs:
    #     bfs(startPuzzle)
    # elif isUcost:
    #     ucost(startPuzzle)
    # elif isGreedy:
    #     greedy(startPuzzle)
    # elif isAstar:
    #     astar(startPuzzle)
    # else:
    #     return -1

    num = ['531246780', '531204786', '543206718', '514203786', '436528710', '436502718', '543726018', '462503718',
            '042563718', '436520718']

    print("search, cost, frontier, expanded")

    for item in num:
        puzz = EightPuzzleBoard(item)
        print("bfs, ", end="")
        bfs(puzz)
    for item in num:
        puzz = EightPuzzleBoard(item)
        print("ucost, ", end="")
        ucost(puzz)
    for item in num:
        puzz = EightPuzzleBoard(item)
        print("greedy, ", end="")
        greedy(puzz)
    for item in num:
        puzz = EightPuzzleBoard(item)
        print("astar, ", end="")
        astar(puzz)

if __name__ == "__main__":
    main()
