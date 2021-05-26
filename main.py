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
    board = ganh(board, (x2, y2))
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


def vay(board, player):
    # vay này chưa đúng
    # enemy = -1 * player
    # for i in range(0, 5):
    #     for j in range(0, 5):
    #         if board[i][j] == enemy:
    #             hints = moveHint(board, (i, j))
    #             print(hints)
    #             if hints == []:
    #                 board[i][j] = player
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
    # => (i+j) mod 2 == 0 => /
    # => |i-j| mod 2 == 0 => \
    # up
    # ex: (1,1) --> (0,1) | (i,j) --> (i-1,j)
    if pos[0] > 0 and board[pos[0]-1][pos[1]] == 0:
        clone = board_clone(board)
        end = (pos[0] - 1, pos[1])
        temp = updateBoard(clone, start, end)
        point = remainingTroop(temp, board[pos[0]][pos[1]])
        hints.append([point, start, end])

    # down
    # ex: (1,1) --> (2,1) | (i,j) --> (i+1,j)
    if pos[0] < 4 and board[pos[0]+1][pos[1]] == 0:
        clone = board_clone(board)
        end = (pos[0] + 1, pos[1])
        temp = updateBoard(clone, start, end)
        point = remainingTroop(temp, board[pos[0]][pos[1]])
        hints.append([point, start, end])

    # left
    # ex: (1,1) --> (1,0) | (i,j) --> (i,j-1)
    if pos[1] > 0 and board[pos[0]][pos[1]-1] == 0:
        clone = board_clone(board)
        end = (pos[0], pos[1]-1)
        temp = updateBoard(clone, start, end)
        point = remainingTroop(temp, board[pos[0]][pos[1]])
        hints.append([point, start, end])

    # right
    # ex: (1,1) --> (1,2) | (i,j) --> (i,j+1)
    if pos[1] < 4 and board[pos[0]][pos[1]+1] == 0:
        clone = board_clone(board)
        end = (pos[0], pos[1]+1)
        temp = updateBoard(clone, start, end)
        point = remainingTroop(temp, board[pos[0]][pos[1]])
        hints.append([point, start, end])

    if (pos[0] + pos[1]) % 2 == 0:
        # up_left
        # ex: (1,1) --> (0,0) | (i,j) --> (i-1,j-1)
        if pos[0] > 0 and pos[1] > 0 and board[pos[0]-1][pos[1]-1] == 0:
            clone = board_clone(board)
            end = (pos[0]-1, pos[1]-1)
            temp = updateBoard(clone, start, end)
            point = remainingTroop(temp, board[pos[0]][pos[1]])
            hints.append([point, start, end])

        # up_right
        # ex: (1,1) --> (0,2) | (i,j) --> (i-1,j+1)
        if pos[0] > 0 and pos[1] < 4 and board[pos[0]-1][pos[1]+1] == 0:
            clone = board_clone(board)
            end = (pos[0]-1, pos[1]+1)
            temp = updateBoard(clone, start, end)
            point = remainingTroop(temp, board[pos[0]][pos[1]])
            hints.append([point, start, end])

        # down_left
        # ex: (1,1) --> (2,0) | (i,j) --> (i+1,j-1)
        if pos[0] < 4 and pos[1] > 0 and board[pos[0]+1][pos[1]-1] == 0:
            clone = board_clone(board)
            end = (pos[0]+1, pos[1]-1)
            temp = updateBoard(clone, start, end)
            point = remainingTroop(temp, board[pos[0]][pos[1]])
            hints.append([point, start, end])

        # down_right
        # ex: (1,1) --> (2,2) | (i,j) --> (i+1,j+1)
        if pos[0] < 4 and pos[1] < 4 and board[pos[0]+1][pos[1]+1] == 0:
            clone = board_clone(board)
            end = (pos[0]+1, pos[1]+1)
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
    while step < 100:
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


def main():
    """
        O : 1
        X : -1 
    """
    # board = board_initial()
    # a = board_clone(board)
    # print(a)
    win = main2()
    if win == 1:
        print("O: win")
    else:
        print("X: win")


if __name__ == '__main__':
    main()
