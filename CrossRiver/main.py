import sys
from CrossRiver.setup import setParameter

def main(N: int, M: int, mode: bool, alg: str):
    Node = setParameter(N, M, mode = mode, alg = alg)
    start = Node()

    if alg == 'AS':
        path = start.AStartSearch()['path']
    if alg == 'UC':
        path = start.uniformCost()['path']

    for node in path:
        print(node.state, node.move, node.total_cost)

if __name__ == '__main__':
    N, M, mode, alg = None, None, None, None

    try:
        for arg in sys.argv[1:]:
            if arg[:2] == '-N':
                N = int(arg[2:])
            elif arg[:2] == '-M':
                M = int(arg[2:])
            elif arg[:2] == '-m':
                mode = int(arg[2:])
            elif arg[:2] == '-a':
                alg = arg[2:]
            else:
                exit(1)
    except:
        raise Exception("Invalid parameter")

    if mode == None or N == None or M == None or alg == None:
        raise Exception("Missing parameter")

    valid = mode in [0, 1] and N in range(3, 11) and M in range(0, 3) and alg in ['AS', 'UC']
    assert valid, 'Invalid Parameter'

    main(N, M, mode, alg)
