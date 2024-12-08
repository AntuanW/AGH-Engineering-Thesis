class Interface:
    def __init__(self, name):
        self.name = name.lower()

    def get_short_name(self):
        if self.name.startswith("gigabitethernet"):
            return "GE" + self.name[15:]
        elif self.name.startswith("fastethernet"):
            return "FE" + self.name[12:]
        elif self.name.startswith("tengigabitethernet"):
            return "TE" + self.name[18:]
        elif self.name.startswith("serial"):
            return "S" + self.name[6:]
        elif self.name.startswith("pc"):
            return "PC" + self.name[2:]
        return self.name
