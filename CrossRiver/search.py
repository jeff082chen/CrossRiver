import bisect

def UniformCost(start):
    '''
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

    while True:

        if not open:
            break

        current = open.pop(0)
        print("current:", current.state, current.total_cost)

        if current.isTarget():
            path = []
            while current.parent != None:
                path.append(current)
                current = current.parent
            path.append(current)
            path.reverse()
            return path

        close.append(current)

        # current is already recorded as parent when creating
        children = current.allValidChild()

        if not children:
            continue

        print('nodes:', sorted([(node.state, node.total_cost) for node in children], key = lambda node: node[0]))

        for child in children:
            if child not in open and child not in close:
                bisect.insort(open, child)
            elif child in open:
                idx = open.index(child)
                if child.total_cost < open[idx].total_cost:
                    open.pop(idx)
                    bisect.insort(open, child)
        
        print('open:', [(node.state, node.total_cost) for node in open])
        print('close:', [(node.state, node.total_cost) for node in close])
        print()

    return None

