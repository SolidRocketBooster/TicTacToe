import socket, re


class Game:
    board = []
    x = 3
    y = 3
    count = 3
    players = [[], []]
    HOST = ""
    PORT = "61780"
    MODE = ""
    sym = ""
    num = ""
    winner = ""
    game_mode = ""


    def __init__(self):
        self.set_board()
        return 1

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
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[i])):
                cell = self.board[i][j]
                if cell == "|_|":
                    score = 1
                    for l, m in map([0, 1, 1, 0, -1, -1, 1, -1], [+1, 0, 1, -1, 0, -1, -1, 1]):
                        for k in range(1, self.count):
                            if cell == self.matrix[i + k * l][j + k * m]:
                                score += 1
                        if score == self.count:
                            self.winner = cell
                            return 1
                        else:
                            score = 1
        return 0

    def player(self, x, y):
        self.players[self.num].append({"sym": self.sym, "board": self.board, "x": x, "y": y})
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
        self.game_mode = input('Choose number: ')
        if game_mode == 1:
            self.game_mode = "local"
        elif game_mode == 2:
            self.game_mode = "online"
            print("""===================================================================
            
            1. Host Game
            2. Join Game
            """)
            if_server = input('Choose number:')
            if if_server == 1:
                self.MODE = "server"
            else:
                self.MODE = "client"

    def get_input(self):
        check = re.compile(f"^[1-{self.count}]$")
        input = ""
        while input == "":
            input = input("Enter number: ")
            if re.match(check, input) == None:
                input == ""
            else:
                return int(input)

    def run(self):
        self.print_board()
        running = True
        self.menu()
        while running:
            if game_mode == "local":
                for num in [1, 2]:
                    for player in self.players:
                        print(f'###### Player {num} ######')
                        user_x = self.get_input()
                        user_y = self.get_input()
                        self.set_cell(user_x, user_y, player["sym"])
                        self.print_board()

            if self.check_win() != 0:
                print("There i a winner")


if __name__ == "__main__":
    app = Game()
    app.run()
