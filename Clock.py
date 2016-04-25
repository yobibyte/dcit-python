class Clock:

    def __init__(self, id):
        self.val = 1
        self.id = id

    def get_val(self):
        return {"id":self.id, "val":self.val}

    def tick(self):
        self.val += 1

    def set_clock(self, val):
        self.val = val

    def compareTo(self, c):
        id = c[0]
        v = c[1]

        if self.val == v and self.id == id:
            return 0

        if self.val == v:
            if self.id > id:
                return 1
            else:
                return -1

        if self.val < v:
            return -1
        else:
            return 1
