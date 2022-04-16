
def generate_all_possible_moves(N, M, boatA_capacity, boatB_capacity):
    temp = []
    for i in range(N + 1):
        for j in range(N + M + 1):
            temp.append(hex(i)[2:] + hex(j)[2:])

    all_possible_moves = []

    for i in temp:
        for j in temp:
            all_possible_moves.append('1' + i + '1' + j)

    for i in temp:
        all_possible_moves.append('000' + '1' + i)
        all_possible_moves.append('1' + i + '000')

    # total cannibals <= N, total missionaries <= N + M
    all_possible_moves = [move for move in all_possible_moves if 
        (int(move[1], 16) + int(move[4], 16) <= N) and (int(move[2], 16) + int(move[5], 16) <= (N + M))
    ]

    # on boatA, cannibals <= missionaries or missionaries = 0, or boatA do not move
    all_possible_moves = [move for move in all_possible_moves if 
        (int(move[2], 16) >= int(move[1], 16)) or (int(move[2], 16) == 0 and int(move[1], 16) > 0) or move[0] == '0'
    ]

    # same above for boatB
    all_possible_moves = [move for move in all_possible_moves if 
        (int(move[5], 16) >= int(move[4], 16)) or (int(move[5], 16) == 0 and int(move[4], 16) > 0) or move[3] == '0'
    ]

    # if boatA move, 1 <= people <= boatA_capacity
    all_possible_moves = [move for move in all_possible_moves if 
        (1 <= int(move[1], 16) + int(move[2], 16) <= boatA_capacity) or move[0] == '0'
    ]

    # if boatB move, 1 <= people <= boatB_capacity
    all_possible_moves = [move for move in all_possible_moves if 
        (1 <= int(move[4], 16) + int(move[5], 16) <= boatB_capacity) or move[3] == '0'
    ]

    return all_possible_moves



def set_parameter(N: int, M: int, /, mode: bool):
    ''' return a class that construct each state in searching
    cannibals: N
    missionaries: N + M
    mode: 0 -> minimun price, 1 -> minimun time
    '''

    valid = mode in [0, 1] and N in range(3, 11) and M in range(0, 3)
    assert valid, 'Invalid Parameter Error'

    boatA_capacity = 2
    boatB_capacity = 3

    boatA_cost = 3
    boatB_cost = 25

    def price(self, move: str) -> int:
        cost = 0
        if move[0] == '1':
            cost += boatA_cost
        if move[3] == '1':
            cost += boatB_cost
        return cost

    def time(self, move: str) -> int:
        if move[0] == '1' or move[3] == '1':
            return 1
        return 0

    # [0]: 1 -> boatA move, 0 -> boatA not move
    # [1:2]: number of cannibal/missionary on boatA
    # [3]: 1 -> boatB move, 0 -> boatB not move
    # [4:5]: number of cannibal/missionary on boatB
    all_possible_moves = generate_all_possible_moves(N, M, boatA_capacity, boatB_capacity)

    state = hex(N)[2:] + hex(N + M)[2:] + '11'

    class node:

        def __init__(self, /, state = state, total_cost = 0, parent = None, move = None):
            self.cannibal_count = N
            self.missionary_count = N + M

            # [0]: cannibals in right
            # [1]: missionaries in right
            # [2]: boatA in right
            # [3]: boatB in right
            self.state = state
            self.move = move

            self.total_cost = total_cost
            self.parent = parent

            self.all_possible_moves = all_possible_moves

        def isValidMove(self, move: str) -> bool:
            
            current_right_cannibals = int(self.state[0], 16)
            current_left_cannibals = N - int(self.state[0], 16)
            assert 0 <= current_right_cannibals <= N, "Invalid State Error"

            current_right_missionaries = int(self.state[1], 16)
            current_left_missionaries = N + M - int(self.state[1], 16)
            assert 0 <= current_right_missionaries <= (N + M), "Invalid State Error"

            cannibals_move_to_right = 0
            cannibals_move_to_left = 0
            missionaries_move_to_right = 0
            missionaries_move_to_left = 0

            if move[0] == '1':
                if (self.state[2] == '1'): # boatA from r to l
                    cannibals_move_to_left += int(move[1], 16)
                    missionaries_move_to_left += int(move[2], 16)
                elif (self.state[2] == '0'): # boatA from r to l
                    cannibals_move_to_right += int(move[1], 16)
                    missionaries_move_to_right += int(move[2], 16)

            if move[3] == '1':
                if (self.state[3] == '1'): # boatB from r to l
                    cannibals_move_to_left += int(move[4], 16)
                    missionaries_move_to_left += int(move[5], 16)
                elif (self.state[3] == '0'): # boatA from r to l
                    cannibals_move_to_right += int(move[4], 16)
                    missionaries_move_to_right += int(move[5], 16)

            if current_right_cannibals < cannibals_move_to_left:
                return False
            if current_left_cannibals < cannibals_move_to_right:
                return False
            if current_right_missionaries < missionaries_move_to_left:
                return False
            if current_left_missionaries < missionaries_move_to_right:
                return False

            right_cannibals = current_right_cannibals - cannibals_move_to_left + cannibals_move_to_right
            left_cannibals = current_left_cannibals - cannibals_move_to_right + cannibals_move_to_left
            right_missionaries = current_right_missionaries - missionaries_move_to_left + missionaries_move_to_right
            left_missionaries = current_left_missionaries - missionaries_move_to_right + missionaries_move_to_left
            if right_cannibals > right_missionaries and right_missionaries != 0:
                return False
            if left_cannibals > left_missionaries and left_missionaries != 0:
                return False

            return True

        def state_after_move(self, move) -> str:

            current_right_cannibals = int(self.state[0], 16)
            assert 0 <= current_right_cannibals <= N, "Invalid State Error"

            current_right_missionaries = int(self.state[1], 16)
            assert 0 <= current_right_missionaries <= (N + M), "Invalid State Error"

            cannibals_move_to_right = 0
            cannibals_move_to_left = 0
            missionaries_move_to_right = 0
            missionaries_move_to_left = 0
            boatA_in_right = 0
            boatB_in_right = 0

            if move[0] == '1':
                if (self.state[2] == '1'): # boatA from r to l
                    boatA_in_right = 0
                    cannibals_move_to_left += int(move[1], 16)
                    missionaries_move_to_left += int(move[2], 16)
                elif (self.state[2] == '0'): # boatA from r to l
                    boatA_in_right = 1
                    cannibals_move_to_right += int(move[1], 16)
                    missionaries_move_to_right += int(move[2], 16)

            if move[3] == '1':
                if (self.state[3] == '1'): # boatB from r to l
                    boatB_in_right = 0
                    cannibals_move_to_left += int(move[4], 16)
                    missionaries_move_to_left += int(move[5], 16)
                elif (self.state[3] == '0'): # boatA from r to l
                    boatB_in_right = 1
                    cannibals_move_to_right += int(move[4], 16)
                    missionaries_move_to_right += int(move[5], 16)

            right_cannibals = current_right_cannibals - cannibals_move_to_left + cannibals_move_to_right
            right_missionaries = current_right_missionaries - missionaries_move_to_left + missionaries_move_to_right
            
            return hex(right_cannibals)[2:] + hex(right_missionaries)[2:] + str(boatA_in_right) + str(boatB_in_right)

        def isTarget(self) -> bool:
            return self.state == '0000'

        def allValidChild(self) -> list:
            result = []
            for move in self.all_possible_moves:
                if self.isValidMove(move):
                    state = self.state_after_move(move)
                    total_cost = self.total_cost + self.calculate_cost(move)
                    result.append(node(state = state, total_cost = total_cost, parent = self, move = move))
            return result

        calculate_cost = price if mode == 0 else time

        def __eq__(self, other) -> bool:
            if other is None:
                return False
            return self.__hash__() == other.__hash__()

        def __lt__(self, other) -> bool:
            return self.total_cost < other.total_cost

        def __hash__(self) -> int:
            return int(self.state, 16)

    return node
