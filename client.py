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
            payload = json.dumps(msg).encode("utf-8")
            s.sendall(payload)
            data = s.recv(1024)
            self.board = json.loads(data.decode("uft-8"))

    def run(self):
        self.print_board()
        
        while not self.connected:
            print("Connecting...")
            msg = json.dumps({"type": "add_player", "num": self.num, "sym": self.sym}).encode("utf-8")
            self.client(msg)

    
if __name__ == "__main__":
    app = Game()
    app.run()
