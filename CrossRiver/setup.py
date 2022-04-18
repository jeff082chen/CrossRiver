from CrossRiver.search import uniformCost, AStartSearch

def generateAllPossibleMoves(N, M, boatA_capacity, boatB_capacity):
    temp = []
    for i in range(N + 1):
        for j in range(N + M + 1):
            temp.append(hex(i)[2:] + hex(j)[2:])

    all_possible_moves = []

    for i in temp:
        for j in temp:
            all_possible_moves.append(i + j)

    for i in temp:
        all_possible_moves.append('00' + i)
        all_possible_moves.append(i + '00')

    # total cannibals <= N, total missionaries <= N + M
    all_possible_moves = [move for move in all_possible_moves if 
        (int(move[0], 16) + int(move[2], 16) <= N) and (int(move[1], 16) + int(move[3], 16) <= (N + M))
    ]

    # on boatA, cannibals <= missionaries or missionaries = 0, or boatA do not move
    all_possible_moves = [move for move in all_possible_moves if 
        (int(move[1], 16) >= int(move[0], 16)) or int(move[1], 16) == 0 or move[:2] == '00'
    ]

    # same above for boatB
    all_possible_moves = [move for move in all_possible_moves if 
        (int(move[3], 16) >= int(move[2], 16)) or int(move[3], 16) == 0 or move[2:] == '00'
    ]

    # if boatA move, 1 <= people <= boatA_capacity
    all_possible_moves = [move for move in all_possible_moves if 
        (1 <= int(move[0], 16) + int(move[1], 16) <= boatA_capacity) or move[:2] == '00'
    ]

    # same above for boatB
    all_possible_moves = [move for move in all_possible_moves if 
        (1 <= int(move[2], 16) + int(move[3], 16) <= boatB_capacity) or move[2:] == '00'
    ]

    return all_possible_moves



# class factories for the nodes
def setParameter(N: int, M: int, /, mode: bool, alg: str):
    ''' return a class that construct each state in searching
    cannibals: N
    missionaries: N + M
    mode: 0 -> minimun price, 1 -> minimun time
    '''

    valid = mode in [0, 1] and N in range(3, 11) and M in range(0, 3)
    assert valid, 'Invalid Parameter Error'

    # set parameters
    boatA_capacity = 2
    boatB_capacity = 3
    boatA_cost = 3
    boatB_cost = 25
    state = '11' + hex(N)[2:] + hex(N + M)[2:]

    # [0:1]: number of cannibal/missionary on boatA
    # [2:3]: number of cannibal/missionary on boatB
    all_possible_moves = generateAllPossibleMoves(N, M, boatA_capacity, boatB_capacity)

    def price(self, move: str) -> int:
        cost = 0
        if move[:2] != '00':
            cost += boatA_cost
        if move[2:] != '00':
            cost += boatB_cost
        return cost

    def time(self, move: str) -> int:
        if move[:2] == '00' and move[2:] == '00':
            return 0
        return 1

    def heuristics_time(self) -> int:
        return (int(self.state[2], 16) + int(self.state[3], 16)) / boatB_capacity

    def heuristics_price(self) -> int:
        return (heuristics_time(self) // 2) * (boatA_cost + boatB_cost) + (heuristics_time(self) % 2) * boatA_cost

    class Node:

        def __init__(self, /, state = state, total_cost = 0, parent = None, move = None):
            self.cannibal_count = N
            self.missionary_count = N + M

            # [0]: boatA in right
            # [1]: boatB in right
            # [2]: cannibals in right
            # [3]: missionaries in right
            self.state = state
            self.move = move

            self.total_cost = total_cost
            self.parent = parent

            self.all_valid_moves = [move for move in all_possible_moves if self.isValidMove(move)]

        # convert state string into number
        def convertState(self):
            cannibals_r = int(self.state[2], 16)
            cannibals_l = N - int(self.state[2], 16)
            assert 0 <= cannibals_r <= N, "Invalid State Error"

            missionaries_r = int(self.state[3], 16)
            missionaries_l = N + M - int(self.state[3], 16)
            assert 0 <= missionaries_r <= (N + M), "Invalid State Error"

            return cannibals_r, cannibals_l, missionaries_r, missionaries_l

        # convert move string into number
        def convertMove(self, move):
            cannibals_to_right = 0
            cannibals_to_left = 0
            missionaries_to_right = 0
            missionaries_to_left = 0

            boatA_in_right = self.state[0] == '1'
            boatB_in_right = self.state[1] == '1'

            if (boatA_in_right): # boatA from r to l
                cannibals_to_left += int(move[0], 16)
                missionaries_to_left += int(move[1], 16)
            else: # boatA from r to l
                cannibals_to_right += int(move[0], 16)
                missionaries_to_right += int(move[1], 16)

            if (boatB_in_right): # boatB from r to l
                cannibals_to_left += int(move[2], 16)
                missionaries_to_left += int(move[3], 16)
            else: # boatA from r to l
                cannibals_to_right += int(move[2], 16)
                missionaries_to_right += int(move[3], 16)

            return cannibals_to_right, cannibals_to_left, missionaries_to_right, missionaries_to_left

        def isValidMove(self, move: str) -> bool:
            
            cannibals_r, cannibals_l, missionaries_r, missionaries_l = self.convertState()
            cannibals_to_r, cannibals_to_l, missionaries_to_r, missionaries_to_l = self.convertMove(move)

            if cannibals_r < cannibals_to_l:
                return False
            if cannibals_l < cannibals_to_r:
                return False
            if missionaries_r < missionaries_to_l:
                return False
            if missionaries_l < missionaries_to_r:
                return False

            right_cannibals = cannibals_r - cannibals_to_l + cannibals_to_r
            left_cannibals = cannibals_l - cannibals_to_r + cannibals_to_l
            right_missionaries = missionaries_r - missionaries_to_l + missionaries_to_r
            left_missionaries = missionaries_l - missionaries_to_r + missionaries_to_l
            if right_cannibals > right_missionaries and right_missionaries != 0:
                return False
            if left_cannibals > left_missionaries and left_missionaries != 0:
                return False

            return True

        def stateAfterMove(self, move) -> str:

            cannibals_r, _, missionaries_r, _ = self.convertState()
            cannibals_to_r, cannibals_to_l, missionaries_to_r, missionaries_to_l = self.convertMove(move)

            cannibals_r = cannibals_r - cannibals_to_l + cannibals_to_r
            missionaries_r = missionaries_r - missionaries_to_l + missionaries_to_r

            if move[:2] != '00':
                boatA_in_right = '1' if self.state[0] == '0' else '0'
            else:
                boatA_in_right = self.state[0]

            if move[2:] != '00':
                boatB_in_right = '1' if self.state[1] == '0' else '0'
            else:
                boatB_in_right = self.state[1]

            return boatA_in_right + boatB_in_right + hex(cannibals_r)[2:] + hex(missionaries_r)[2:]

        def isTarget(self) -> bool:
            return self.state[2:] == '00'

        def allValidChild(self) -> list:
            result = []
            for move in self.all_valid_moves:
                state = self.stateAfterMove(move)
                total_cost = self.total_cost + self.cost(move)
                result.append(Node(state = state, total_cost = total_cost, parent = self, move = move))
            return result

        def path(self):
            path = []
            current = self
            while current.parent != None:
                path.append(current)
                current = current.parent
            path.append(current)
            path.reverse()
            return path

        cost = price if mode == 0 else time
        h = heuristics_price if mode == 0 else heuristics_time

        def __eq__(self, other) -> bool:
            if other is None:
                return False
            return self.__hash__() == other.__hash__()

        if alg == 'AS':
            def __lt__(self, other) -> bool:
                if self.total_cost + self.h() == other.total_cost + other.h():
                    return self.h() < other.h()
                return self.total_cost + self.h() < other.total_cost + other.h()
        elif alg == 'UC':
            def __lt__(self, other) -> bool:
                return self.total_cost < other.total_cost

        def __hash__(self) -> int:
            return int(self.state, 16)

        def uniformCost(self):
            return uniformCost(self)

        def AStartSearch(self):
            return AStartSearch(self)

    return Node
