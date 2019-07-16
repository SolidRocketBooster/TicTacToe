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
            per_data = s.recv(1024)
            data = json.loads(per_data)
        print(data)
        self.board = data[0]
        return data[1]

    def join(self):
        print("Enter a player number and sumbol that you wish to use.")
        while self.num == "":
            temp = input("Enter a player number: ")
            if temp is [1, 2]:
                self.num = temp
            else:
                print("Wrong input")



    def run(self):
        self.print_board()
        
        while not self.connected:
            print("Connecting...")
            msg = {"type": "add_player", "num": self.num, "sym": self.sym}
            print(type(msg))
            response = self.client(msg)
            print(response)
            if response == 1:
                self.connected = True
            else:

    
if __name__ == "__main__":
    app = Game()
    app.run()
