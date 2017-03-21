class T0:
    def __init__(self, x, y):
        self.status = 0
        self.x = x
        self.y = y

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

    def get_pos(self):
        return self.x, self.y


class T1:
    def __init__(self, x_pos, y_pos):
        self.winner = None
        self.x = x_pos
        self.y = y_pos
        self.t0s = []
        for x in range(3):
            rows = []
            for y in range(3):
                rows.append(T0(x, y))
            self.t0s.append(rows)

    def get_t0s(self):
        return self.t0s

    def get_t0_at(self, x, y):
        return self.t0s[x][y]

    def check_for_winner(self):
        for i in range(3):
            if self.t0s[i][0].get_status() == self.t0s[i][1].get_status() == self.t0s[i][2].get_status():
                if self.t0s[i][0].get_status():
                    return self.t0s[i][0].get_status()
        for i in range(3):
            if self.t0s[0][i].get_status() == self.t0s[1][i].get_status() == self.t0s[2][i].get_status():
                if self.t0s[0][i].get_status():
                    return self.t0s[0][i].get_status()

        if self.t0s[0][0].get_status() == self.t0s[1][1].get_status() == self.t0s[2][2].get_status():
            if self.t0s[0][0].get_status():
                return self.t0s[0][0].get_status()

        if self.t0s[0][2].get_status() == self.t0s[1][1].get_status() == self.t0s[2][0].get_status():
            if self.t0s[0][2].get_status():
                return self.t0s[0][2].get_status()

    def get_winner(self):
        if not self.winner:
            if self.check_for_winner():
                self.winner = self.check_for_winner()
        return self.winner

    def get_pos(self):
        return self.x, self.y


class T2:
    def __init__(self, x_pos, y_pos):
        self.winner = None
        self.x = x_pos
        self.y = y_pos
        self.t1s = []
        for x in range(3):
            rows = []
            for y in range(3):
                rows.append(T1(x, y))
            self.t1s.append(rows)

    def get_t1s(self):
        return self.t1s

    def get_t1_at(self, x, y):
        return self.t1s[x][y]

    def get_winner(self):
        return self.winner

    def get_pos(self):
        return self.x, self.y


class T3:
    def __init__(self):
        self.winner = None
        self.t2s = []
        for x in range(3):
            rows = []
            for y in range(3):
                rows.append(T2(x, y))
            self.t2s.append(rows)

    def get_t2s(self):
        return self.t2s

    def get_t2_at(self, x, y):
        return self.t2s[x][y]

    def get_winner(self):
        return self.winner
