

class Game:

    def __init__(self, player1, player2):
        self.players = [player1, player2]
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
