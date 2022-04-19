import bisect

def uniformCost(start, /, debug = False):
    '''
    pseudocode code:
    1.   function UCS(Graph, start, target):
    2.      Add the starting node to the opened list. The node has
    3.      has zero distance value from itself
    4.      while True:
    5.         if opened is empty:
    6.            break # No solution found
    7.         selecte_node = remove from opened list, the node with
    8.                        the minimun distance value
    9.         if selected_node == target:
    10.           calculate path
    11.           return path
    12.        add selected_node to closed list
    13.        new_nodes = get the children of selected_node
    14.        if the selected node has children:
    15.           for each child in children:
    16.              calculate the distance value of child
    17.              if child not in closed and opened lists:
    18.                 child.parent = selected_node
    19.                 add the child to opened list
    20.              else if child in opened list:
    21.                 if the distance value of child is lower than 
    22.                  the corresponding node in opened list:
    23.                    child.parent = selected_node
    24.                    add the child to opened list
    '''

    open = [start]
    close = []

    # count loop
    count = 0

    while open:
        count += 1
        current = open.pop(0)

        if debug:
            print("current:", current.state, current.total_time, current.total_price)

        if current.isTarget():
            # print out the value of count
            print('count:', count)
            return {'path': current.path(), 'count': count}

        close.append(current)

        # current is already recorded as parent when creating
        children = current.allValidChild()

        if debug:
            print('nodes:', sorted([(node.state, node.total_time, node.total_price) for node in children], key = lambda node: node[0]))

        for child in children:
            if child.over_cost():
                continue
            if child not in open and child not in close:
                bisect.insort(open, child)
            elif child in open:
                idx = open.index(child)
                if child.total_cost() < open[idx].total_cost():
                    open.pop(idx)
                    bisect.insort(open, child)
        
        if debug:
            print('open:', [(node.state, node.total_time, node.total_price) for node in open])
            print('close:', [(node.state, node.total_time, node.total_price) for node in close])
            print()

    if debug:
        print('count:', count)
    return None





def AStartSearch(start, /, debug = False):
    '''
    Add START to OPEN list
    while OPEN not empty
        get node n from OPEN that has the lowest f(n)
        if n is GOAL then return path
        move n to CLOSED
        for each n' = CanMove(n , direction)
            g(n') = g(n) + cost(n,n')
            calculate f(n')=g(n')+h(n')
            if n' in OPEN list and new n' is not better , continue
            if n' in CLOSED list and new n' is not better , continue
            remove any n' from OPEN and CLOSED
            add n as n's parent
            add n' to OPEN …從OPEN 開始   
        end for
    end while
    if we get here , then there is No Solution
    '''

    open = [start]
    close = []

    # count loop
    count = 0

    while open:
        count += 1
        current = open.pop(0)

        if debug:
            print("current:", current.state, current.total_time, current.total_price)

        if current.isTarget():
            return {'path': current.path(), 'count': count}

        bisect.insort(close, current)

        # current is already recorded as parent when creating
        children = current.allValidChild()

        if debug:
            print('nodes:', sorted([(node.state, node.total_time, node.total_price) for node in children], key = lambda node: node[0]))
            print()

        for child in children:

            if child.over_cost():
                continue

            if child in open and child.total_cost() >= open[open.index(child)].total_cost():
                continue
            if child in close and child.total_cost() >= close[close.index(child)].total_cost():
                continue
            
            if child in open:
                open.pop(open.index(child))
            if child in close:
                close.pop(close.index(child))

            bisect.insort(open, child)

        if debug:
            print('open:', [(node.state, node.total_time, node.total_price) for node in open], '\n')
            print('close:', [(node.state, node.total_time, node.total_price) for node in close], '\n')
            print()
            
    return None
