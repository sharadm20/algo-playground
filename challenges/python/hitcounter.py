class HitCounter:
    def __init__(self, hit):
        self.hit = hit
    def record(self, timestamp):
        value = self.hit[timestamp]
        self.hit[timestamp] = value + 1
    def total(self):
        return sum(self.hit.values())
    def range(self, lower, upper):
        res = []
        for key, val in self.hit.items():
            i = 0
            if int(key) >= lower and int(key) <= upper:
                res[i] = val
                i = i+1
        return sum(res)
    