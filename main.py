import bisect
from node import node

def UniformCost(start: node):

    open = [start]
    close = []

    while True:

        if not open:
            break

        current = open.pop()

        if current.isTarget():
            return current.path + [current]

        close.append(current)

        children = current.allValidChild()

        for child in children:

            if child not in open and child not in close:
                child.path.append(current)
                bisect.insort(open, child)

            elif child in open:

                idx = open.index(child)

                if child.cost() < open[idx].cost():
                    child.path.append(open[idx])
                    open.pop(idx)
                    bisect.insort(open, child)
    return None

