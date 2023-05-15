'''
    AI 2023
    แก้ code ได้เฉพาะใน file นี้เท่านั้น
    จะเพิ่ม function ก็สามารถทำได้นะ แต่ชื่อ class กับชื่อ findBestMove method ห้ามแก้เด็ดขาด
    นอกนั้น ทำได้หมด จะเพิ่มตัวแปรก็ทำได้
    ห้ามใช้ library ที่ อจ ต้อง install เพิ่มเติมจากที่กำหนดให้
'''
import copy
import random
from board import Board
from time import time
# use deepcopy to copy a list เนื่องจาก list ใน python ส่งค่าแบบ pass by reference
# ดังนั้นเราเลยต้องใช้ deepcopy function ใน copy เพื่อให้เป็นการส่งค่า pass by value แทน


MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]


# ห้ามแก้ชื่อ class
class ComputeOthello:

    # ห้ามแก้ __init__ method
    def __init__(self, board, num_tiles, n=8):
        self.board = board
        self.num_tiles = num_tiles
        self.time_play = [0, 0]
        self.n = n
        self.current_player = 0
        self.opponent = 1
        self.conner = False

    def make_move(self):
        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.num_tiles[self.current_player] += 1
            self.flip_tiles()

    def flip_tiles(self):
        curr_tile = self.current_player + 1
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(self.move, direction):
                i = 1
                while True:
                    row = self.move[0] + direction[0] * i
                    col = self.move[1] + direction[1] * i
                    if self.board[row][col] == curr_tile:
                        break
                    else:
                        self.board[row][col] = curr_tile
                        self.num_tiles[self.current_player] += 1
                        self.num_tiles[(self.current_player + 1) % 2] -= 1
                        i += 1

    def has_tile_to_flip(self, move, direction):
        i = 1
        if self.current_player in (0, 1) and \
           self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player + 1
            while True:
                row = move[0] + direction[0] * i
                col = move[1] + direction[1] * i
                if not self.is_valid_coord(row, col) or \
                        self.board[row][col] == 0:
                    return False
                elif self.board[row][col] == curr_tile:
                    break
                else:
                    i += 1
        return i > 1

    def has_legal_move(self):
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    return True
        return False

    def get_legal_moves(self):
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    moves.append(move)

        if self.conner:
            connerset = [0, 7]
            result = [sublist for sublist in moves if any(
                item in sublist for item in connerset)]
            if result:
                return result
        return moves

    def is_legal_move(self, move):
        if move != () and self.is_valid_coord(move[0], move[1]) \
           and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False

    def is_valid_coord(self, row, col):
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False


    # Evaluation weights for different positions on the board
    evaluation_weights = [
        [120, -20,  20,   5,   5,  20, -20, 120],
        [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
        [20,  -5,  15,   3,   3,  15,  -5,  20],
        [5,  -5,   3,   3,   3,   3,  -5,   5],
        [5,  -5,   3,   3,   3,   3,  -5,   5],
        [20,  -5,  15,   3,   3,  15,  -5,  20],
        [-20, -40,  -5,  -5,  -5,  -5, -40, -20],
        [120, -20,  20,   5,   5,  20, -20, 120]
    ]


    def evaluate(self,board, player):
        score = 0
        #opponent = self.board.get_opponent(player)
        for i in range(8):
            for j in range(8):
                #  if board.board[i][j] == player:
                score += self.evaluation_weights[i][j]
                # elif board.board[i][j] == opponent:
                #     score -= evaluation_weights[i][j]
        return score

        # Aplha Beta Pruning
        # ทำ function นี้ให้สมบูรณ์
        # ห้ามแก้ชื่อ function และตัว arguments ที่เป็น input ของ function

    def findBestMove(self,board, current_player, opponent, num_tiles):
        self.board = board
        self.num_tiles = num_tiles
        self.current_player = current_player
        self.opponent = opponent
         
        def minimax(board, depth, alpha, beta, maximizing_player):
            if depth == 0 or not self.has_legal_move() or num_tiles == 64:
                return self.evaluate(board, self.current_player)

            if maximizing_player:
                max_eval = float('-inf')
                valid_moves = self.get_legal_moves()
                for move in valid_moves:
                    new_board = copy.deepcopy(board)
                    #new_board.make_move(current_player, move)
                    eval = minimax(new_board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                return max_eval
            else:
                min_eval = float('inf')
                for move in self.get_legal_moves():
                    new_board = copy.deepcopy(board)
                    #new_board.make_move(opponent, move)
                    eval = minimax(new_board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                return min_eval

        best_move = None
        max_eval = float('-inf')
        valid_moves = self.get_legal_moves()
        for move in valid_moves:
            new_board = copy.deepcopy(board)
            #new_board.make_move(current_player, move)
            eval = minimax(new_board, 3, float('-inf'), float('inf'), False)
            if eval > max_eval:
                max_eval = eval
                best_move = move

        return best_move
        
    #     best_move = None
    #     max_eval = float('-inf')
    #     valid_moves = self.get_legal_moves()
    #     for move in valid_moves:
    #         new_board = copy.deepcopy(board)
    #         eval = minimax(new_board, 3, float('-inf'), float('inf'), False,False,False)
    #         if eval > max_eval:
    #             max_eval = eval
    #             best_move = move

    #     return best_move

    # def minimax(board, depth, alpha, beta, maximizing_player,current_player,num_tiles,opponent):
    #         if depth == 0 or board.is_game_over() or num_tiles == 64:
    #             return evaluate(board, current_player)

    #         if maximizing_player:
    #             max_eval = float('-inf')
    #             for move in board.get_valid_moves(current_player):
    #                 new_board = copy.deepcopy(board)
    #                 new_board.make_move(current_player, move)
    #                 eval = minimax(new_board, depth - 1, alpha, beta, False)
    #                 max_eval = max(max_eval, eval)
    #                 alpha = max(alpha, eval)
    #                 if beta <= alpha:
    #                     break
    #             return max_eval
    #         else:
    #             min_eval = float('inf')
    #             for move in board.get_valid_moves(opponent):
    #                 new_board = copy.deepcopy(board)
    #                 new_board.make_move(opponent, move)
    #                 eval = minimax(new_board, depth - 1, alpha, beta, True)
    #                 min_eval = min(min_eval, eval)
    #                 beta = min(beta, eval)
    #                 if beta <= alpha:
    #                     break
    #             return min_eval




        