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
            data = json.JSONDecoder().decode(s.recv(1024))
            self.board = data[0]
            return data[1]

    def run(self):
        self.print_board()
        
        while not self.connected:
            print("Connecting...")
            msg = json.JSONEncoder().encode({"type": "add_player", "num": self.num, "sym": self.sym})
            print(type(msg))
            response = self.client(msg)
            if response == 1:
                self.connected = True

    
if __name__ == "__main__":
    app = Game()
    app.run()
