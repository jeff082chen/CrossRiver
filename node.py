

class node:

    def __init__(self):
        self.state = '00000000'
        self.cost = 0
        self.path = []

    def isTarget(self) -> bool:
        pass

    def allValidChild(self) -> list:
        pass

    def cost(self, parent) -> int:
        pass

    def __eq__(self, other) -> bool:
        pass

    def __lt__(self, other) -> bool:
        pass