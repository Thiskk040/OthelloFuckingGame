'''
    adapted from https://github.com/SiyanH/othello-game
    ห้ามแก้ใน file นี้
'''

import turtle, random,copy
from time import time
from board import Board
from findbestmove import ComputeOthello

# Define all the possible directions in which a player's move can flip 
# their adversary's tiles as constant (0 – the current row/column, 
# +1 – the next row/column, -1 – the previous row/column)
MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]

class Othello(Board):
    ''' Othello class.
        Attributes: current_player, an integer 0 or 1 to represent two 
                    different players (the user and the computer)
                    num_tiles, a list of integers for number of tiles each 
                    player has
                    n, an integer for nxn board
                    all other attributes inherited from class Board
        n (integer) is optional in the __init__ function
        current_player, num_tiles and all other inherited attributes 
        are not taken in the __init__

        Methods: initialize_board, make_move, flip_tiles, has_tile_to_flip, 
                 has_legal_move, get_legal_moves, is_legal_move, 
                 is_valid_coord, run, play, make_random_move, 
                 report_result, __str__ , __eq__ and all other methods 
                 inherited from class Board
    '''

    def __init__(self, playmode, n = 8):
        '''
            Initilizes the attributes. 
            Only takes one optional parameter; others have default values.
        '''
        Board.__init__(self, n)
        self.current_player = 0
        self.num_tiles = [2, 2]
        self.count = 0
        self.time_play = [0,0]
        self.max_time = 120
        self.playmode = playmode

    def initialize_board(self):
        ''' Method: initialize_board
            Parameters: self
            Returns: nothing
            Does: Draws the first 4 tiles in the middle of the board
                  (the size of the board must be at least 2x2).
        '''
        if self.n < 2:
            return

        coord1 = int(self.n / 2 - 1)
        coord2 = int(self.n / 2)
        initial_squares = [(coord1, coord2), (coord1, coord1),
                           (coord2, coord1), (coord2, coord2)]
        
        for i in range(len(initial_squares)):
            color = i % 2
            row = initial_squares[i][0]
            col = initial_squares[i][1]
            self.board[row][col] = color + 1
            self.draw_tile(initial_squares[i], color)
    
    def make_move(self):
        ''' Method: make_move
            Parameters: self
            Returns: nothing
            Does: Draws a tile for the player's next legal move on the 
                  board and flips the adversary's tiles. Also, updates the 
                  state of the board (1 for black tiles and 2 for white 
                  tiles), and increases the number of tiles of the current 
                  player by 1.
        '''
        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.num_tiles[self.current_player] += 1
            self.draw_tile(self.move, self.current_player)
            self.flip_tiles()
            
            # print(self.__str__())
    

    def flip_tiles(self):
        ''' Method: flip_tiles
            Parameters: self
            Returns: nothing
            Does: Flips the adversary's tiles for current move. Also, 
                  updates the state of the board (1 for black tiles and 
                  2 for white tiles), increases the number of tiles of 
                  the current player by 1, and decreases the number of 
                  tiles of the adversary by 1.
        '''
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
                        self.draw_tile((row, col), self.current_player)
                        i += 1

    def has_tile_to_flip(self, move, direction):
        ''' Method: has_tile_to_flip
            Parameters: self, move (tuple), direction (tuple)
            Returns: boolean 
                     (True if there is any tile to flip, False otherwise)
            Does: Checks whether the player has any adversary's tile to flip
                  with the move they make.

                  About input: move is the (row, col) coordinate of where the 
                  player makes a move; direction is the direction in which the 
                  adversary's tile is to be flipped (direction is any tuple 
                  defined in MOVE_DIRS).
        '''
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
        ''' Method: has_legal_move
            Parameters: self
            Returns: boolean 
                     (True if the player has legal move, False otherwise)
            Does: Checks whether the current player has any legal move 
                  to make.
        '''
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    return True
        return False
    
    def get_legal_moves(self):
        ''' Method: get_legal_moves
            Parameters: self
            Returns: a list of legal moves that can be made
            Does: Finds all the legal moves the current player can make.
                  Every move is a tuple of coordinates (row, col).
        '''
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    moves.append(move)
        return moves

    def is_legal_move(self, move):
        ''' Method: is_legal_move
            Parameters: self, move (tuple)
            Returns: boolean (True if move is legal, False otherwise)
            Does: Checks whether the player's move is legal.

                  About input: move is a tuple of coordinates (row, col).
        '''
        if move != () and self.is_valid_coord(move[0], move[1]) \
           and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False

    def is_valid_coord(self, row, col):
        ''' Method: is_valid_coord
            Parameters: self, row (integer), col (integer)
            Returns: boolean (True if row and col is valid, False otherwise)
            Does: Checks whether the given coordinate (row, col) is valid.
                  A valid coordinate must be in the range of the board.
        '''
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False

    # ทำการเริ่มตั้น run game
    def run(self):
        ''' Method: run
            Parameters: self
            Returns: nothing
            Does: Starts the game, sets the user to be the first player,
                  and then alternate back and forth between the user and 
                  the computer until the game is over.
        '''
        if self.current_player not in (0, 1):
            print('Error: unknown player. Quit...')
            return
        
        self.current_player = 0
        self.opponent = 1
        if self.playmode == 'com':
            self.computeothello = ComputeOthello(self.board,self.num_tiles,8)
            self.play_computer()
        else:
            print('Your turn.')
            turtle.onscreenclick(self.play)

        turtle.mainloop()

    def play_computer(self):
        ''' Method: play_computer
            Parameters: self
            Returns: nothing
            Does: Plays alternately between the computers.  
        '''
        # ถ้าเล่นกับคอมพิวเตอร์ ต้องกำหนดว่า com แต่ละตัวเล่นยังไง
        if self.current_player ==0:
            start = time()
            #findBestMove method ต้องคืนค่า (row,col) ออกมาว่าจะลงที่ตำแหน่งใด
            #self.make_random_move()
            self.move = self.computeothello.findBestMove(copy.deepcopy(self.board),self.current_player,self.opponent,
                                     copy.deepcopy(self.num_tiles))
            end = time()
            if self.move:
                self.make_move()
        else:
            start = time()
            #self.make_random_move()
            #self.move = self.computeothello.findBestMove(copy.deepcopy(self.board),self.current_player,self.opponent,
            #                          copy.deepcopy(self.num_tiles))
            self.move = self.computeothello.findBestMove(copy.deepcopy(self.board),self.current_player,self.opponent,
                                        copy.deepcopy(self.num_tiles))
            end = time()
            if self.move:
                self.make_move()

        self.time_play[self.current_player] += end - start

        # สำหรับ debug 
        # print(self.__str__())

        #  ทำการสลับกันเล่น
        self.current_player,self.opponent = (self.opponent,self.current_player)
        
        # Check whether the game is over
        if sum(self.num_tiles) == self.n ** 2 or self.count == 5:
            turtle.onscreenclick(None)
            print('-----------')
            self.report_result()
            print(self.time_play)
           
        elif self.time_play[0] > self.max_time or self.time_play[1] > self.max_time:
            # ถ้ามีทีมใดใช้เวลาในการเล่นเกิน 120 วินาที จะโดนปรับแพ้
            if self.time_play[0] > self.max_time:
                print('2 wins!!! 1 spends time more than 120 seconds')
            elif self.time_play[1] > self.max_time:
                print('1 wins!!! 2 spends time greater than 120 seconds')
            
            print(self.time_play)

        elif not self.has_legal_move():
            # ถ้า player คนนั้นเล่นไม่ได้แล้ว ไม่มีที่จะลง ให้ pass และให้อีกคนเล่นแทน ทำแบบนี้ไปได้ 5 ครั้ง
            self.count += 1
            print("current player: "+ str(self.current_player)+" pass this turn")
            self.current_player,self.opponent = (self.opponent,self.current_player)
            self.play_computer()
        else:
            self.play_computer()
    

    def play(self, x, y):
        ''' Method: play
            Parameters: self, x (float), y (float)
            Returns: nothing
            Does: Plays alternately between the user's turn and the computer's
                  turn. The user plays the first turn. For the user's turn, 
                  gets the user's move by their click on the screen, and makes 
                  the move if it is legal; otherwise, waits indefinitely for a 
                  legal move to make. For the computer's turn, just makes a 
                  random legal move. If one of the two players (user/computer)
                  does not have a legal move, switches to another player's 
                  turn. When both of them have no more legal moves or the 
                  board is full, reports the result, saves the user's score 
                  and ends the game.

                  About the input: (x, y) are the coordinates of where 
                  the user clicks.
        '''
        # Play the user's turn
        if self.has_legal_move():
            self.get_coord(x, y)
            if self.is_legal_move(self.move):
                turtle.onscreenclick(None)
                self.make_move()
            else:
                return

        # Play the computer's turn
        while True:
            self.current_player = 1
            if self.has_legal_move():
                print('Computer\'s turn.')
                # for debugging 
                print(self.__str__())
                self.make_random_move()
                if self.move:
                    self.make_move()
                self.current_player = 0
                if self.has_legal_move():  
                    break
            else:
                break
        
        # Switch back to the user's turn
        self.current_player = 0

        # Check whether the game is over
        if not self.has_legal_move() or sum(self.num_tiles) == self.n ** 2:
            turtle.onscreenclick(None)
            print('-----------')
            self.report_result()
            
        else:
            print('Your turn.')
            turtle.onscreenclick(self.play)
        
    def make_random_move(self):
        ''' Method: make_random_move
            Parameters: self
            Returns: nothing
            Does: Makes a random legal move on the board.
        '''
        moves = self.get_legal_moves()
        if moves:
            self.move = random.choice(moves)

    def report_result(self):
        ''' Method: report_result
            Parameters: self
            Returns: nothing
            Does: Announces the winner and reports the final number of
                  tiles each play has.
        '''
        print('GAME OVER!!')
        if self.num_tiles[0] > self.num_tiles[1]:
            print('Player 1 WIN!!',
                  'Player 1 has %d tiles, but Player 2 only has %d!' 
                  % (self.num_tiles[0], self.num_tiles[1]))
        elif self.num_tiles[0] < self.num_tiles[1]:
            print('Player 2 WIN!!',
                  'Player 2 has %d tiles, but Player 1 only has %d :(' 
                  % (self.num_tiles[1], self.num_tiles[0]))
        else:
            print("IT'S A TIE!! There are %d of each!" % self.num_tiles[0])
            if self.time_play[0] > self.time_play[1]:
                print('Player 2 WIN!!', 'Player 2 played faster than Player 1')
            else:
                print('Player 1 WIN!!', 'Player 1 played faster than Player 2')
    
    
    def __str__(self):
        ''' 
            Returns a printable version of the current status of the 
            game to print.
        '''
        player_str = 'Current player: ' + str(self.current_player + 1) + '\n'
        num_tiles_str = '# of black tiles -- 1: ' + str(self.num_tiles[0]) + \
                        '\n' + '# of white tiles -- 2: ' + \
                        str(self.num_tiles[1]) + '\n'
        board_str = Board.__str__(self)
        printable_str = player_str + num_tiles_str + board_str

        return printable_str

    def __eq__(self, other):
        '''
            Compares two instances. 
            Returns True if they have both the same board attribute and 
            current player, False otherwise.
        '''
        return Board.__eq__(self, other) and self.current_player == \
        other.current_player
