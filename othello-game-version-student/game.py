'''
    adapted from https://github.com/SiyanH/othello-game
    We can choose between 'com' (com vs com) and 'user' (com vs user)
    Player 1 สีดำ (user) และ Player 2 สีขาว (com)
    ห้ามแก้ใน file นี้

    ขั้นตอนการรัน python ใน vs code
    1. install python 3.11 ลงเครื่อง 
    2. ใน vs code: select interpreter เป็น python 3.11
    3. ใน vs code: install python extension
    4. เริ่มต้นรันจาก file นี้ โดยกด run and debug
    5. สามารถแก้ args ได้ที่ file: launch.json นะ โดยสามารถเปลี่ยน 'com' (com vs com) หรือ 'user' (com vs user)
'''

import othello
import sys

def main():
    # Initializes the game
    args = sys.argv[1:]
    print(args)
    game = othello.Othello(args[0])
    game.draw_board()
    game.initialize_board()

    # Starts playing the game
    game.run()


main()
