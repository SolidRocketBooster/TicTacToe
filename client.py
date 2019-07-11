import socket, re


class Game:
    board = []
    x = 3
    y = 3
    count = 3
    players = {}
    HOST = ""
    PORT = "61780"
    MODE = ""
    sym = ""
    num = ""
    winner = ""
    game_mode = ""


    def __init__(self):
        self.set_board()

    def set_board(self):
        self.board = [["|_|" for j in range(0, self.x)] for i in range(0, self.y)]
        return 1

    def print_board(self):
        for row in self.board:
            print("".join(row))
        return 1

    def set_cell(self, x, y, sym):
        if self.board[x][y] == "|_|":
            self.board[x][y] = sym
            return 1
        else:
            return 0

    def check_win(self):
        for row in range(0, len(self.board)):
            for column in range(0, len(self.board[i])):
                cell = self.board[i][j]
                if cell == "|_|":
                    score = 1
                    for rowMod, columnMod in zip([0, 1, 1, 0, -1, -1, 1, -1], [+1, 0, 1, -1, 0, -1, -1, 1]):
                        for distanceCounter in range(1, self.count):
                            if cell == self.board[row + distanceCounter * rowMod][column + distanceCounter * columnMod]:
                                score += 1
                        if score == self.count:
                            self.winner = cell
                            return 1
                        else:
                            score = 1
        return 0

    def player(self, num, sym):
        self.players[self.num] = sym
        return 1

    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    self.player()
                    conn.sendall(self.board)


    def client(self):
        frame = players[self.num]
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(frame)
            self.board = s.recv(1024)

    def menu(self):
        print("""===================================================================
Choose game mode

1. Local
2. Online
""")
        inp = self.get_input('Choose number: ', 2)
        if inp == 1:
            self.game_mode = "local"
            sym = ["O", "X"]
            print(f"""Player 1 will use
1. O or 2. X
""")
            choice = self.get_input("Enter 1 or 2: ")
            self.player(1, sym.pop(choice - 1))
            self player(2, sym.pop())
            print(f"Player 1 will use {players[0]}")
            print(f"Player 2 will use {players[1]}")
                
        elif inp == 2:
            self.game_mode = "online"
            print("""===================================================================
            
1. Host Game
2. Join Game
""")
            if_server = self.get_input('Choose number: ', 2)
            if if_server == 1:
                self.MODE = "server"
            else:
                self.MODE = "client"

    def get_input(self, mesg="", max=9):
        inp = ""
        while inp == "":
            inp = int(input(mesg))
            if inp in range(1, max + 1):
                return inp
            else:
                print("Wrong input!")
                inp = ""

    def run(self):
        self.print_board()
        running = True
        self.menu()
        while running:
            if self.game_mode == "local":
                for player in self.players:
                    print(f'###### Player {num} ######')
                    user_x = self.get_input("Enter Column number: ", self.count)
                    user_y = self.get_input("Enter Row number: ", self.count)
                    self.set_cell(user_x, user_y, player)
                    self.print_board()

            if self.check_win() == 1:
                print("There i a winner")
                running = False


if __name__ == "__main__":
    app = Game()
    app.run()
