import sys
from CrossRiver.setup import setParameter

def main(N: int, M: int, mode: bool, alg: str, debug: bool, limit: int):
    Node = setParameter(N, M, mode = mode, alg = alg, debug = debug, limit = limit)
    start = Node()

    if alg == 'AS':
        result = start.AStartSearch()
    if alg == 'UC':
        result = start.uniformCost()

    if result:
        print('count:', result['count'])
        for node in result['path']:
            print(node.state, node.move, node.total_price, node.total_time)
    else:
        print('No Solution')

if __name__ == '__main__':
    N, M, mode, alg = None, None, None, None
    debug = False
    limit = None

    try:
        for arg in sys.argv[1:]:
            if arg[:2] == '-N':
                assert N is None, Exception("Duplicate argument")
                N = int(arg[2:])
            elif arg[:2] == '-M':
                assert M is None, Exception("Duplicate argument")
                M = int(arg[2:])
            elif arg == '-p' or arg == '-t':
                assert mode is None, Exception("Duplicate argument")
                mode = arg[-1]
            elif arg == '-AS' or arg == '-UC':
                assert alg is None, Exception("Duplicate argument")
                alg = arg[1:]
            elif arg == '-d':
                assert debug == False, Exception("Duplicate argument")
                debug = True
            elif arg[:2] == '-l':
                assert limit is None, Exception("Duplicate argument")
                limit = int(arg[2:])
            else:
                exit(1)
    except Exception("Duplicate argument"):
        exit(1)
    except:
        raise Exception("Invalid parameter")

    if mode == None or N == None or M == None or alg == None:
        raise Exception("Missing parameter")

    valid = mode in ['p', 't'] and N in range(3, 11) and M in range(0, 3) and alg in ['AS', 'UC']
    assert valid, 'Invalid Parameter'

    main(N, M, mode, alg, debug, limit = limit)
