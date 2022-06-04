import argparse
from CrossRiver.setup import setParameter

parser = argparse.ArgumentParser(description = 'Missionaries and Cannibals Problem', prog = "CrossRiver")
parser.add_argument('N', type = int, default = 3, help = 'N: integer between 3 and 10', choices = range(3, 11))
parser.add_argument('M', type = int, default = 0, help = 'M: integer between 0 and 2', choices = range(0, 3))
parser.add_argument('--debug', '-d', action = 'store_true', help = 'debug mode')
parser.add_argument('--limit', '-l', type = int, default = None, help = 'limit: price limit when mode is time, and vice versa', metavar = 'lim')

mode = parser.add_mutually_exclusive_group(required = True)
mode.add_argument('--time', '-t', action = 'store_true', help = 'mode: time')
mode.add_argument('--price', '-p', action = 'store_true', help = 'mode: price')

alg = parser.add_mutually_exclusive_group(required = True)
alg.add_argument('-AS', action = 'store_true', help = 'A* Search')
alg.add_argument('-UC', action = 'store_true', help = 'Uniform Cost')

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

    args = parser.parse_args()

    args.mode = 't' if args.time else 'p'
    args.alg = 'AS' if args.AS else 'UC'

    valid = args.mode in ['p', 't'] and args.N in range(3, 11) and args.M in range(0, 3) and args.alg in ['AS', 'UC']
    assert valid, 'Invalid Parameter'

    main(args.N, args.M, args.mode[0], args.alg, args.debug, limit = args.limit)
