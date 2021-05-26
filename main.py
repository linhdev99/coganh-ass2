import time
import copy
import random
import math


def board_initial():
    board = [
        [1,  1,  1,  1,  1],
        [1,  0,  0,  0,  1],
        [-1,  0,  0,  0,  1],
        [-1,  0,  0,  0, -1],
        [-1, -1, -1, -1, -1]
    ]
    return board


def board_clone(board):
    clone = []
    for i in range(0, 5):
        clone.append([])
        for j in range(0, 5):
            clone[i].append(board[i][j])
    return clone


def updateBoard(board, start, end):
    x1, y1 = start
    x2, y2 = end
    board[x2][y2] = board[x1][y1]
    board[x1][y1] = 0
    # printBoard(board)
    board = ganh(board, (x2, y2))
    board = vay(board, board[x2][y2])
    return board


def ganh(board, current):
    player = board[current[0]][current[1]]
    # check row
    if current[1] > 0 and current[1] < 4:
        enemy1 = board[current[0]][current[1]-1]
        enemy2 = board[current[0]][current[1]+1]
        if enemy1 == player*(-1) and enemy2 == player*(-1):
            board[current[0]][current[1]-1] = player
            board[current[0]][current[1]+1] = player
    # check col
    if current[0] > 0 and current[0] < 4:
        enemy1 = board[current[0]-1][current[1]]
        enemy2 = board[current[0]+1][current[1]]
        if enemy1 == player*(-1) and enemy2 == player*(-1):
            board[current[0]-1][current[1]] = player
            board[current[0]+1][current[1]] = player

    # check cross line
    if (current[0]+current[1]) % 2 == 0 and current[0] > 0 and current[0] < 4 and current[1] > 0 and current[1] < 4:
        enemy1 = board[current[0]-1][current[1]-1]
        enemy2 = board[current[0]+1][current[1]+1]
        if enemy1 == player*(-1) and enemy2 == player*(-1):
            board[current[0]-1][current[1]-1] = player
            board[current[0]+1][current[1]+1] = player
        enemy1 = board[current[0]-1][current[1]+1]
        enemy2 = board[current[0]+1][current[1]-1]
        if enemy1 == player*(-1) and enemy2 == player*(-1):
            board[current[0]-1][current[1]+1] = player
            board[current[0]+1][current[1]-1] = player

    return board


def findNeighbor(board, pos):
    enemy = board[pos[0]][pos[1]]
    # print(enemy)
    neighbor = []
    if pos[0] > 0 and board[pos[0]-1][pos[1]] == enemy:
        neighbor.append((pos[0]-1, pos[1]))

    # down
    # ex: (1,1) --> (2,1) | (i,j) --> (i+1,j)
    if pos[0] < 4 and board[pos[0]+1][pos[1]] == enemy:
        neighbor.append((pos[0]+1, pos[1]))

    # left
    # ex: (1,1) --> (1,0) | (i,j) --> (i,j-1)
    if pos[1] > 0 and board[pos[0]][pos[1]-1] == enemy:
        neighbor.append((pos[0], pos[1]-1))

    # right
    # ex: (1,1) --> (1,2) | (i,j) --> (i,j+1)
    if pos[1] < 4 and board[pos[0]][pos[1]+1] == enemy:
        neighbor.append((pos[0], pos[1]+1))

    if (pos[0] + pos[1]) % 2 == enemy:
        # up_left
        # ex: (1,1) --> (0,0) | (i,j) --> (i-1,j-1)
        if pos[0] > 0 and pos[1] > 0 and board[pos[0]-1][pos[1]-1] == enemy:
            neighbor.append((pos[0]-1, pos[1]-1))

        # up_right
        # ex: (1,1) --> (0,2) | (i,j) --> (i-1,j+1)
        if pos[0] > 0 and pos[1] < 4 and board[pos[0]-1][pos[1]+1] == enemy:
            neighbor.append((pos[0]-1, pos[1]+1))

        # down_left
        # ex: (1,1) --> (2,0) | (i,j) --> (i+1,j-1)
        if pos[0] < 4 and pos[1] > 0 and board[pos[0]+1][pos[1]-1] == enemy:
            neighbor.append((pos[0]+1, pos[1]-1))

        # down_right
        # ex: (1,1) --> (2,2) | (i,j) --> (i+1,j+1)
        if pos[0] < 4 and pos[1] < 4 and board[pos[0]+1][pos[1]+1] == enemy:
            neighbor.append((pos[0]+1, pos[1]+1))

    # print(neighbor)
    return neighbor


def findHint(board, pos):
    hints = []  # [point, start, end]
    start = (pos[0], pos[1])
    if pos[0] > 0 and board[pos[0]-1][pos[1]] == 0:
        end = (pos[0] - 1, pos[1])
        hints.append(end)

    # down
    # ex: (1,1) --> (2,1) | (i,j) --> (i+1,j)
    if pos[0] < 4 and board[pos[0]+1][pos[1]] == 0:
        end = (pos[0] + 1, pos[1])
        hints.append(end)

    # left
    # ex: (1,1) --> (1,0) | (i,j) --> (i,j-1)
    if pos[1] > 0 and board[pos[0]][pos[1]-1] == 0:
        end = (pos[0], pos[1]-1)
        hints.append(end)

    # right
    # ex: (1,1) --> (1,2) | (i,j) --> (i,j+1)
    if pos[1] < 4 and board[pos[0]][pos[1]+1] == 0:
        end = (pos[0], pos[1]+1)
        hints.append(end)

    if (pos[0] + pos[1]) % 2 == 0:
        # up_left
        # ex: (1,1) --> (0,0) | (i,j) --> (i-1,j-1)
        if pos[0] > 0 and pos[1] > 0 and board[pos[0]-1][pos[1]-1] == 0:
            end = (pos[0]-1, pos[1]-1)
            hints.append(end)

        # up_right
        # ex: (1,1) --> (0,2) | (i,j) --> (i-1,j+1)
        if pos[0] > 0 and pos[1] < 4 and board[pos[0]-1][pos[1]+1] == 0:
            end = (pos[0]-1, pos[1]+1)
            hints.append(end)

        # down_left
        # ex: (1,1) --> (2,0) | (i,j) --> (i+1,j-1)
        if pos[0] < 4 and pos[1] > 0 and board[pos[0]+1][pos[1]-1] == 0:
            end = (pos[0]+1, pos[1]-1)
            hints.append(end)

        # down_right
        # ex: (1,1) --> (2,2) | (i,j) --> (i+1,j+1)
        if pos[0] < 4 and pos[1] < 4 and board[pos[0]+1][pos[1]+1] == 0:
            end = (pos[0]+1, pos[1]+1)
            hints.append(end)

    return hints


def depthNeighbor(board, pos, closed=[]):
    canMove = False
    i, j = pos
    hint = findHint(board, (i, j))
    if hint != []:
        return True
    else:
        neighbor = []
        fNeighbor = findNeighbor(board, (i, j))
        # print("==========")
        # print(pos, fNeighbor, closed)
        # print(closed)
        # print(fNeighbor)
        for per in fNeighbor:
            if not per in closed:
                neighbor.append(per)
        # print(neighbor)
        # print("==========")
        if neighbor == []:
            return False
        else:
            # print("pos", pos)
            if not pos in closed:
                closed.append(pos)
            for per in neighbor:
                # print(per)
                canMove = depthNeighbor(board, per, closed)
                # print(canMove)
                # print("========")
                if canMove:
                    return True
            return False


def vay(board, player):
    # vay này chưa đúng
    enemy = -1 * player
    closed = []
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == enemy:
                # print((i,j), board[i][j])
                canMove = depthNeighbor(board, (i, j), [])
                # print(canMove)
                if not canMove:
                    closed.append((i, j))
    for per in closed:
        board[per[0]][per[1]] = player
    return board


def remainingTroop(board, player):
    totalTroop = 0
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == player:
                totalTroop += 1
    return totalTroop


def moveHint(board, pos):
    hints = []  # [point, start, end]
    start = (pos[0], pos[1])
    hintList = findHint(board, start)
    for end in hintList:
        clone = board_clone(board)
        temp = updateBoard(clone, start, end)
        point = remainingTroop(temp, board[pos[0]][pos[1]])
        hints.append([point, start, end])
    return hints


def move(board, player):
    maxPoint = 0
    start = None
    end = None
    savePoint = []
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == player:
                hints = moveHint(board, (i, j))
                for hint in hints:
                    # print(hint[0])
                    if hint[0] == maxPoint:
                        savePoint.append(hint)
                        maxPoint = hint[0]
                    if hint[0] > maxPoint:
                        savePoint.clear()
                        savePoint.append(hint)
                        maxPoint = hint[0]
    # print("==================")
    if savePoint == []:
        return None
    else:
        idx = random.randint(0, len(savePoint)-1)
        hint = savePoint[idx]
        start = hint[1]
        end = hint[2]
        return (start, end)


def printBoard(board):
    for i in range(0, 5):
        print("%d\t%d\t%d\t%d\t%d" %
              (board[i][0], board[i][1], board[i][2], board[i][3], board[i][4]))


def main2(first='X'):
    board = board_initial()
    step = 0
    while step < 1000:
        step += 1
        p1 = remainingTroop(board, 1)
        p2 = remainingTroop(board, -1)
        if p1 == 16:
            return 1
        if p2 == 16:
            return -1
        if first == 'X':
            temp = move(board, -1)
            if temp == None:
                return 1
            else:
                print(first, temp)
                board = updateBoard(board, temp[0], temp[1])
            first = 'O'
        elif first == 'O':
            temp = move(board, 1)
            if temp == None:
                return -1
            else:
                print(first, temp)
                board = updateBoard(board, temp[0], temp[1])
            first = 'X'
        printBoard(board)
        print("=======")

def test():
    board = [
        [1,  -1,  -1,  -1,  1],
        [1,  0,  0,  0,  1],
        [1,  0,  -1,  0,  0],
        [-1,  0,  0,  1, -1],
        [-1, -1, -1, 0, -1]
    ]
    printBoard(board)
    print('=============')
    board = updateBoard(board, (2,0), (3,1))
    printBoard(board)

def main():
    """
        O : 1
        X : -1 
    """
    test()
    # win = main2('X')
    # print(win)
    # board = board_initial()
    # a = board_clone(board)
    # print(a)
    # count = 0
    # for x in range(0, 100):
    #     win = main2('X')
    #     if win == 1:
    #         continue
    #         # print("O: win")
    #     else:
    #         count += 1
    #         # print("X: win")
    # print("X win %d" % (count), "%")


if __name__ == '__main__':
    main()
