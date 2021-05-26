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
    return board


def ganh(board, current):
    # check row

    # check col

    # check cross line
    return board


def vay(board):
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
    for i in range(0, 5):
        for j in range(0, 5):
            if board[i][j] == player:
                hints = moveHint(board, (i, j))
                for hint in hints:
                    print(hint)
                    # if hint[0] > maxPoint:
                    #     maxPoint = hint[0]
                    #     start = hint[1]
                    #     end = hint[2]
    if start == None:
        return None
    else:
        return (start, end)


def main2(first='X'):
    board = board_initial()
    while True:
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
                updateBoard(board, temp[0], temp[1])
            first = 'O'
        elif first == 'O':
            temp = move(board, 1)
            if temp == None:
                return -1
            else:
                updateBoard(board, temp[0], temp[1])
            first = 'X'


def main():
    """
        O : 1
        X : -1 
    """
    # board = board_initial()
    # a = board_clone(board)
    # print(a)
    print(main2())


if __name__ == '__main__':
    main()
