import time
import copy
import random

COUNT = 0


class Node:
    def __init__(self, player, cur_board, depth=0):
        self.board = cur_board
        self.value = cur_board.getPoint(player)
        self.previous = None
        self.next = []
        self.depth = depth

    def insert(self, player, board, depth=0):
        element = Node(board, player)
        self.next.append(element)
        self.depth = depth

    def printTree(self):
        print("print tree...")
        f = open("tree.txt", "w")
        global COUNT
        f.write("COUNT: " + str(COUNT))
        f.close()
        self.printFile()
    
    def printFile(self):
        f = open("tree.txt", "r")
        old_s = f.read()
        f.close()
        f = open("tree.txt", "w")
        # print("depth:", self.depth, ", value:", self.value, "-----------")
        new_s = ""
        for i in range(0, self.depth):
            new_s = new_s + "__"
        new_s = new_s + "depth: " + str(self.depth) + \
                ", value: " + str(self.value) + " -------"
        new_s = old_s + "\n" + new_s
        board = self.board.board
        new_s = new_s + "\n" + "---------------------------------"
        for i in range(0, 5):
            # print(board[i][0])
            board_s = str(board[i][0]) + "\t" + \
                    str(board[i][1]) + "\t" + \
                    str(board[i][2]) + "\t" + \
                    str(board[i][3]) + "\t" + \
                    str(board[i][4]) + "\t"
            new_s = new_s + "\n" + board_s
            # print(board_s)
        new_s = new_s + "\n" + "---------------------------------"
        f.write(new_s)
        # self.board.printBoard()
        # print("-----------------------")
        f.close()
        if self.depth >= 0:
            for ele in self.next:
                ele.printFile()


class AI:
    def __init__(self):
        self.timeStart = time.time()
        self.timeExceeded = False

    def create_tree(self, depth, player, tree=None):
        global COUNT
        if depth == 0:
            return tree
        else:
            if tree == None:
                board = Board()
                board.initialBoard()
                tree = Node(player, board)
            board = tree.board
            hints = board.getAvailableHint(player)
            for hint in hints:
                value = hint[0]
                start = hint[1]
                end = hint[2]
                clone = Board()
                clone.initialBoard()
                clone.setBoard(board.board)
                clone.updateBoard(start, end)
                # print(hint)
                # clone.printBoard()
                element = Node(-1 * player, clone, depth-1)
                element.previous = tree
                tree.next.append(element)
                COUNT += 1
                self.create_tree(depth-1, -1 * player, element)
            return tree
        # print(len(tree.next))

    def alpha_beta_arth():
        pass


class Board:
    def __init__(self):
        self.board = list()
        self.red = 0
        self.blue = 0

    def initialBoard(self):
        self.board = [
            [1,  1,  1,  1,  1],
            [1,  0,  0,  0,  1],
            [-1,  0,  0,  0,  1],
            [-1,  0,  0,  0, -1],
            [-1, -1, -1, -1, -1]
        ]
        self.red = 8
        self.blue = 8

    def setBoard(self, gird):
        self.board = copy.deepcopy(gird)
        self.remainingTroop()

    def getAvailableHint(self, player):
        board = self.board
        hints = []
        for i in range(0, 5):
            for j in range(0, 5):
                if board[i][j] == player:
                    clone = self.board_clone()
                    tempHints = clone.moveHints((i, j))
                    for hint in tempHints:
                        hints.append(hint)
                    # self.printBoard()
                    # print(tempHints)
        # print(hints)
        return hints

    def findHint(self, pos):
        hints = []  # [point, start, end]
        board = self.board
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

    def findNeighbor(self, pos):
        board = self.board
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

    def depthNeighbor(self, pos, closed=[]):
        board = self.board
        canMove = False
        i, j = pos
        hint = self.findHint((i, j))
        if hint != []:
            return True
        else:
            neighbor = []
            fNeighbor = self.findNeighbor((i, j))
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
                    canMove = self.depthNeighbor(per, closed)
                    # print(canMove)
                    # print("========")
                    if canMove:
                        return True
                return False

    def board_clone(self):
        clone = Board()
        # clone.initialBoard()
        # for i in range(0,5):
        #     for j in range(0,5):
        #         clone.board[i][j] = board[i][j]
        clone.board = copy.deepcopy(self.board)
        clone.red = self.red
        clone.blue = self.blue
        return clone

    def ganh(self, pos):
        board = self.board
        player = board[pos[0]][pos[1]]
        # check row
        if pos[1] > 0 and pos[1] < 4:
            enemy1 = board[pos[0]][pos[1]-1]
            enemy2 = board[pos[0]][pos[1]+1]
            if enemy1 == player*(-1) and enemy2 == player*(-1):
                board[pos[0]][pos[1]-1] = player
                board[pos[0]][pos[1]+1] = player
        # check col
        if pos[0] > 0 and pos[0] < 4:
            enemy1 = board[pos[0]-1][pos[1]]
            enemy2 = board[pos[0]+1][pos[1]]
            if enemy1 == player*(-1) and enemy2 == player*(-1):
                board[pos[0]-1][pos[1]] = player
                board[pos[0]+1][pos[1]] = player

        # check cross line
        if (pos[0]+pos[1]) % 2 == 0 and pos[0] > 0 and pos[0] < 4 and pos[1] > 0 and pos[1] < 4:
            enemy1 = board[pos[0]-1][pos[1]-1]
            enemy2 = board[pos[0]+1][pos[1]+1]
            if enemy1 == player*(-1) and enemy2 == player*(-1):
                board[pos[0]-1][pos[1]-1] = player
                board[pos[0]+1][pos[1]+1] = player
            enemy1 = board[pos[0]-1][pos[1]+1]
            enemy2 = board[pos[0]+1][pos[1]-1]
            if enemy1 == player*(-1) and enemy2 == player*(-1):
                board[pos[0]-1][pos[1]+1] = player
                board[pos[0]+1][pos[1]-1] = player

        # return board

    def vay(self, pos):
        board = self.board
        player = board[pos[0]][pos[1]]
        enemy = -1 * player
        closed = []
        for i in range(0, 5):
            for j in range(0, 5):
                if board[i][j] == enemy:
                    # print((i,j), board[i][j])
                    canMove = self.depthNeighbor((i, j), [])
                    # print(canMove)
                    if not canMove:
                        closed.append((i, j))
        for per in closed:
            board[per[0]][per[1]] = player
        # return board

    def remainingTroop(self):
        red = 0
        blue = 0
        for i in range(0, 5):
            for j in range(0, 5):
                if self.board[i][j] == 1:
                    red += 1
                elif self.board[i][j] == -1:
                    blue += 1
        self.red = red
        self.blue = blue

    def getPoint(self, player):
        self.remainingTroop()
        if player == 1:
            return self.red
        elif player == -1:
            return self.blue

    def updateBoard(self, start, end):
        x1, y1 = start
        x2, y2 = end
        board = self. board
        board[x2][y2] = board[x1][y1]
        board[x1][y1] = 0
        # printBoard(board)
        self.ganh((x2, y2))
        self.vay((x2, y2))
        self.remainingTroop()

    def moveHints(self, pos):
        hints = []
        board = self.board
        start = pos
        hintList = self.findHint(start)
        player = board[pos[0]][pos[1]]
        for end in hintList:
            clone = self.board_clone()
            clone.updateBoard(start, end)
            point = clone.red
            if player == -1:
                point == clone.blue
            hints.append([point, start, end])
        return hints

    def printBoard(self):
        board = self.board
        print("---------------------------------")
        for i in range(0, 5):
            print("%d\t%d\t%d\t%d\t%d" %
                  (board[i][0], board[i][1], board[i][2], board[i][3], board[i][4]))
        print("---------------------------------")


class Player:
    def __init__(self):
        self.name = 0
        self.depth = 3
        self.board = Board()
        self.board.initialBoard()
        self.tree = None

    def move(self, cur_board, name):
        self.board.setBoard(cur_board)
        self.name = name
        result = self.next_move()
        return result

    def next_move(self):
        result = tuple()  # (start, end)
        self.tree = Node(self.name, self.board, self.depth)
        ai = AI()
        ai.create_tree(self.depth, self.name, self.tree)
        # global COUNT
        # self.tree.printTree()
        # print(COUNT)

        # self.board.getAvailableHint(self.name)
        return result


def move(board, player):
    troop = Player()
    state = troop.move(board, player)
    return state


def printBoard(board):
    for i in range(0, 5):
        print("%d\t%d\t%d\t%d\t%d" %
              (board[i][0], board[i][1], board[i][2], board[i][3], board[i][4]))


def main2(first='X'):
    board = [
        [1,  1,  1,  1,  1],
        [1,  0,  0,  0,  1],
        [-1,  0,  0,  0,  1],
        [-1,  0,  0,  0, -1],
        [-1, -1, -1, -1, -1]
    ]
    move(board, 1)
    # gird = Board()
    # gird.initialBoard()
    # gird.printBoard()
    # gird.getAvailableHint(1)
    # board = gird.board
    # board = board_initial()
    # step = 0
    # while step < 1000:
    #     step += 1
    #     p1 = remainingTroop(board, 1)
    #     p2 = remainingTroop(board, -1)
    #     if p1 == 16:
    #         return 1
    #     if p2 == 16:
    #         return -1
    #     if first == 'X':
    #         temp = move(board, -1)
    #         if temp == None:
    #             return 1
    #         else:
    #             # print(first, temp)
    #             board = updateBoard(board, temp[0], temp[1])
    #         first = 'O'
    #     elif first == 'O':
    #         temp = move(board, 1)
    #         if temp == None:
    #             return -1
    #         else:
    #             # print(first, temp)
    #             board = updateBoard(board, temp[0], temp[1])
    #         first = 'X'
    #     # printBoard(board)
    #     # print("=======")


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
    board = updateBoard(board, (2, 0), (3, 1))
    printBoard(board)


def main():
    """
        O : 1
        X : -1 
    """
    # test()
    win = main2('O')
    # print(win)
    # board = board_initial()
    # a = board_clone(board)
    # print(a)
    # count = 0
    # for x in range(0, 100):
    #     win = main2('O')
    #     if win == 1:
    #         continue
    #         # print("O: win")
    #     else:
    #         count += 1
    #         # print("X: win")
    # print("X win %d" % (count), "%")


if __name__ == '__main__':
    main()
