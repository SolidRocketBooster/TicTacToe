import socket, json

class Game:
    board = []
    players = {}
    HOST = ""
    PORT = 61780
    current_player = 1


    def __init__(self):
        self.set_board()

    def set_board(self):
        self.board = [["|_|" for j in range(0, 3)] for i in range(0, 3)]
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
                        for distanceCounter in range(1, 3):
                            if cell == self.board[row + distanceCounter * rowMod][column + distanceCounter * columnMod]:
                                score += 1
                        if score == self.count:
                            self.winner = cell
                            return 1
                        else:
                            score = 1
        return 0

    def add_player(self, addr, num, sym, win):
        if num is self.players.keys():
            return "Player already taken."
            if sym in [s[1] for s in self.players.values()]:
                return "Symbol is already taken."
        else:
            self.players[num] = [addr, sym, win]
            return 1

    def server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.HOST, self.PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        result = ""
                        data = json.loads(conn.recv(1024))
                        if not data:
                            break
                        else:
                            print(data)
                            print(type(data))
                            if data["type"] == "add_player":
                                result = self.add_player(addr, data["num"], data["sym"], False)
                                print(f"Result is {result}")
                            elif data["type"] == "set_cell":
                                result = self.set_cell(self.board, data["x"], data["y"], data["sym"])
                                print(f"Result is {result}")
                        payload = json.dumps([self.board, result]).encode("utf-8")
                        print(payload)
                        conn.sendall(payload)
                        break
        except KeyboardInterrupt:
            print("Closing server")
            s.close()


if __name__ == "__main__":
    app = Game()
    app.server()
