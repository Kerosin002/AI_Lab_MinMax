from exceptions import AgentException
import math


class AlphaBetaAgent:
    def __init__(self, token):
        self.my_token = token

    def heuristic(self, s):
        corners = [(0, 0), (0, s.width - 1), (s.height - 1, 0), (s.height - 1, s.width - 1)]
        return 0.2 * sum(1 for row, col in corners if s.board[row][col] == self.my_token)

    def lookForMV(self, x, s, d,a,b):
        ta=a
        tb=b
        mv=0
        k = -1
        if x == 0:
            mv = math.inf
            k = 1
        else:
            mv = -math.inf
            k = 0
        for i in range(len(s.possible_drops())):
            s.drop_token(s.possible_drops()[i])
            result = self.alphabeta(s, k, d - 1,ta,tb)
            s.undo_last_move()
            if x == 0:
                mv = min(result, mv)
                tb=min(tb,mv)
                if mv<=ta:
                    break
            else:
                mv = max(result, mv)
                ta=max(result,mv)
                if mv>=tb:
                    break
        return mv

    def alphabeta(self, s, x, d,a,b):
        if self.my_token == s.wins:
            return 1
        if self.my_token != s.wins and s.wins is not None:
            return -1
        if s.wins is None and s.game_over is True:
            return 0
        if d == 0:
            return self.heuristic(s)
        return self.lookForMV(x, s, d,a,b)

    def decide(self, s):
        if s.who_moves != self.my_token:
            raise AgentException('not my turn')
        x = 1
        d = 4
        mv = -math.inf
        a=-math.inf
        mvs = 0
        for i in range(len(s.possible_drops())):
            s.drop_token(s.possible_drops()[i])
            result = self.alphabeta(s, x, d - 1,a,math.inf)
            s.undo_last_move()
            if result > mv:
                mv = result
                mvs = i
        return s.possible_drops()[mvs]
