

class Preprocessing:
    def __init__(self, filename, scale=100):
        self.A1A2 = 'a1a2'
        self.A1B2 = 'a1b2'
        self.B1A2 = 'b1a2'
        self.B1B2 = 'b1b2'
        self.data = {'a1a2': [], 'b1a2': [], 'b1b2': [], 'a1b2': [], 'time': []}
        self.SCALE = scale
        self.measurements = []
        self.extract_data(filename)

    def extract_distance(self, token, line):
        key_word = 'r_' + token + ' ='
        start = line.find(key_word) + len(key_word) + 1
        end = line.find("mm  at t =")
        return line[start: end]

    def extract_time(self, line):
        key_word = 'current time ='
        start = line.find(key_word) + len(key_word)
        end = line.find("\n")
        return line[start: end]


    def extract_data(self, filename):
        with open(filename) as f:
            lines = f.readlines()

        self.data = {'a1a2': [], 'b1a2': [], 'b1b2': [], 'a1b2': [], 'time': []}

        for i in range(0, len(lines), 4):
            r_a1a2 = self.extract_distance(self.A1A2, lines[i])
            r_b1a2 = self.extract_distance(self.B1A2, lines[i + 1])
            r_a1b2 = self.extract_distance(self.A1B2, lines[i + 2])
            r_b1b2 = self.extract_distance(self.B1B2, lines[i + 3])
            #print(i)



            if 'drop' in r_b1b2 or 'drop' in r_a1b2 or 'drop' in r_a1a2 or 'drop' in r_b1a2:
                continue
            else:
                t_a1a2 = float(self.extract_time(lines[i]))
                t_b1a2 = float(self.extract_time(lines[i + 1]))
                t_a1b2 = float(self.extract_time(lines[i + 2]))
                t_b1b2 = float(self.extract_time(lines[i + 3]))
                self.data[self.A1A2].append(int(r_a1a2) / self.SCALE)
                self.data[self.B1A2].append(int(r_b1a2) / self.SCALE)
                self.data[self.B1B2].append(int(r_b1b2) / self.SCALE)
                self.data[self.A1B2].append(int(r_a1b2) / self.SCALE)
                self.data['time'].append((t_a1a2 + t_b1a2 + t_a1b2 + t_b1b2)/4)
        self.measurements = []
        for a1a2, a1b2, b1a2, b1b2, time in zip(self.data[self.A1A2], self.data[self.A1B2], self.data[self.B1A2], self.data[self.B1B2], self.data['time']):
            self.measurements.append((a1a2, a1b2, b1a2,  b1b2, time))

    def get_all_measurements(self):
        return self.data.copy()


    def get_measurement(self):
        if len(self.measurements) == 0:
            return None
        return self.measurements.pop(0)

