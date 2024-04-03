from exceptions import AgentException
import math


class MinMaxAgent:
    def __init__(self, token):
        self.my_token = token

    def heuristic(self, s):
        corners = [(0, 0), (0, s.width - 1), (s.height - 1, 0), (s.height - 1, s.width - 1)]
        count = sum(1 for row, col in corners if s.board[row][col] == self.my_token)
        return 0.2 * count

    def lookForMV(self, x, s, d):
        mv = 0
        k = -1
        if x == 0:
            mv = math.inf
            k = 1
        else:
            mv = -math.inf
            k = 0
        for i in range(len(s.possible_drops())):
            s.drop_token(s.possible_drops()[i])
            result = self.minmax(s, k, d - 1)
            s.undo_last_move()
            if x == 0:
                mv = min(result, mv)
            else:
                mv = max(result, mv)
        return mv

    def minmax(self, s, x, d):
        if self.my_token == s.wins:
            return 1
        if self.my_token != s.wins and s.wins is not None:
            return -1
        if s.wins is None and s.game_over is True:
            return 0
        if d == 0:
            return self.heuristic(s)
        return self.lookForMV(x, s, d)

    def decide(self, s):
        if s.who_moves != self.my_token:
            raise AgentException('not my turn')
        x = 0
        d = 2
        mv = -math.inf
        mvs = 0
        for i in range(len(s.possible_drops())):
            s.drop_token(s.possible_drops()[i])
            result = self.minmax(s, x, d - 1)
            s.undo_last_move()
            if result > mv:
                mv = result
                mvs = i
        return s.possible_drops()[mvs]
