import socket, json


class Game:
    board = []
    HOST = ""
    PORT = 61780
    connected = False
    sym = ""
    num = ""


    def __init__(self):
        pass

    def print_board(self):
        for row in self.board:
            print("".join(row))
        return 1

    def client(self, msg):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(msg)
            self.board = s.recv(1024)[1]

    def run(self):
        self.print_board()
        
        while not self.connected:
            print("Connecting...")
            msg = bytes({"type": "add_player", "num": self.num, "sym": self.sym})
            self.client(msg)

    
if __name__ == "__main__":
    app = Game()
    app.run()
