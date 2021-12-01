

class Preprocessing:
    def __init__(self, filename, scale=100):
        self.A1A2 = 'a1a2'
        self.A1B2 = 'a1b2'
        self.B1A2 = 'b1a2'
        self.B1B2 = 'b1b2'
        self.data = {'a1a2': [], 'b1a2': [], 'b1b2': [], 'a1b2': []}
        self.SCALE = scale
        self.measurements = []
        self.extract_data(filename)

    def extract_distance(self, token, line):
        key_word = 'r_' + token + ' ='
        start = line.find(key_word) + len(key_word)
        end = line.find("mm  at t =")
        return line[start: end]


    def extract_data(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        self.data = {'a1a2': [], 'b1a2': [], 'b1b2': [], 'a1b2': []}

        for i in range(0, len(lines), 4):
            r_a1a2 = self.extract_distance(self.A1A2, lines[i])
            r_b1a2 = self.extract_distance(self.B1A2, lines[i + 1])
            r_a1b2 = self.extract_distance(self.A1B2, lines[i + 2])
            r_b1b2 = self.extract_distance(self.B1B2, lines[i + 3])
            if 'drop' in  r_b1b2 or 'drop' in r_a1b2 or 'drop' in r_a1a2 or 'drop' in r_b1a2:
                continue
            else:
                self.data[self.A1A2].append(int(r_a1a2) / self.SCALE)
                self.data[self.B1A2].append(int(r_b1a2) / self.SCALE)
                self.data[self.B1B2].append(int(r_b1b2) / self.SCALE)
                self.data[self.A1B2].append(int(r_a1b2) / self.SCALE)
        self.measurements = []
        for a1a2, a1b2, b1a2, b1b2 in zip(self.data[self.A1A2], self.data[self.A1B2], self.data[self.B1A2], self.data[self.B1B2]):
            self.measurements.append((a1a2, a1b2, b1a2,  b1b2))

    def get_all_measurements(self):
        return self.data.copy()


    def get_measurement(self):
        if len(self.measurements) == 0:
            return None
        return self.measurements.pop(0)

