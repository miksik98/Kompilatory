class Memory:

    def __init__(self, name):
        self.name = name  # memory name
        self.variables = {}

    def has_key(self, name):
        if self.variables[name] is None:  # variable name
            return False
        return True

    def get(self, name):
        return self.variables[name]  # gets from memory current value of variable <name>

    def put(self, name, value):
        self.variables[name] = value  # puts into memory current value of variable <name>


class MemoryStack:

    def __init__(self, memory=None):
        self.memory = memory
        self.items = []
        for item in memory.variables.items():
            self.items.append(item)
        # initialize memory stack with memory <memory>

    def get(self, name):
        for i in self.items:
            if i[0] == name:
                return i[1]
        return None
        # gets from memory stack current value of variable <name>

    def insert(self, name, value):
        self.items.append((name, value))  # inserts into memory stack variable <name> with value <value>

    def set(self, name, value):
        item = None
        for i in self.items:
            if i[0] == name:
                item = i
                break
        self.items.remove(item)
        self.items.append((name, value))
        # sets variable <name> to value <value>

    def push(self, memory):
        for item in memory.variables:
            self.items.append(item)  # pushes memory <memory> onto the stack

    def pop(self):
        return self.items.pop()
        # pops the top memory from the stack
