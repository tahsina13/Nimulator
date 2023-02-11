class Nim: 
    balls: list[int]
    rules: list[int]
    
    def __init__(self, balls: list[int] = [], rules: list[int] = []): 
        self.balls = list()
        self.rules = list()
        for i in range(0, len(balls)): 
            if i < len(rules): 
                self.add_col(i, balls[i], rules[i])
            else: 
                self.add_col(i, balls[i])

    def add_col(self, position: int, amount: int = 0, rule: int = 0): 
        self.balls.insert(position, amount)
        self.rules.insert(position, rule)
        
    def remove_col(self, position: int) -> tuple[int, int]: 
        amount = self.balls.pop(position)
        rule = self.rules.pop(position)
        return amount, rule

    def get_limit(self, col: int) -> int: 
        return min(self.balls[col], self.rules[col]) if self.rules[col] else self.balls[col]
        
    def next_move(self) -> tuple[int, int]: 
        state = 0
        nimbers = list()
        for i in range(0, len(self.balls)): 
            nimbers.append([0] * (self.balls[i]+1))
            for j in range(1, self.balls[i]+1): 
                adj = list()
                k = j-1
                while k >= 0 and j-k <= self.get_limit(i): 
                    adj.append(nimbers[i][k])
                    k -= 1
                adj.sort()
                for x in adj: 
                    nimbers[i][j] += x == nimbers[i][j]
            state ^= nimbers[i][-1]
        col, amt = 0, 0
        mn = max(self.balls)+1
        for i in range(0, len(self.balls)): 
            j = 1
            while j <= self.get_limit(i): 
                if state^nimbers[i][-1]^nimbers[i][self.balls[i]-j] < mn: 
                    col, amt = i, j  
                    mn = state^nimbers[i][-1]^nimbers[i][self.balls[i]-j]
                j += 1
        return col, amt

    def is_finished(self): 
        return not any(self.balls)