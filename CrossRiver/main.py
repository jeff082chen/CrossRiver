import sys
from CrossRiver.setup import set_parameter
from CrossRiver.search import UniformCost

def main(N: int, M: int, mode: bool):
    MyClass = set_parameter(N, M, mode = mode)
    start = MyClass()
    path = UniformCost(start)
    for node in path:
        print(node.state, node.move, node.total_cost)

if __name__ == '__main__':
    N, M, mode = None, None, None

    try:
        for arg in sys.argv:
            if arg[:2] == '-N':
                N = int(arg[2:])
            if arg[:2] == '-M':
                M = int(arg[2:])
            if arg[:2] == '-m':
                mode = int(arg[2:])
    except:
        raise Exception("Invalid parameter")

    if mode == None or N == None or M == None:
        raise Exception("Missing parameter")

    valid = mode in [0, 1] and N in range(3, 11) and M in range(0, 3)
    assert valid, 'Invalid Parameter'

    main(N, M, mode)
