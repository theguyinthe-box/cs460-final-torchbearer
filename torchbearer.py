"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: David Kaauwai
Student ID: 826497939

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return """Part 1: Problem Analysis
    - Why a single shortest-path run from S is not enough: The shortest path or the least number of nodes visited by the torchbearer doesn't gurantee that the minimum fuel will consumed, it doesn't even guarantee that the torchbearer will not run out of fuel before it reaches the end. In other words, a single shortest path only reaches one specific node, it doesn't decide which relic to visit first to optimally reserve its fuel. 
    - What decision remains after all inter-location costs are known: The only decision that remains once the torchbearer knows all interlocation costs is to determine the order of the relics it'll be retrieving.
    - Why this requires a search over orders (one sentence): Different permutations of the orders of relics produce different fuel costs, so computing a single path would not be guaranteed to find the route that costs the minimum fuel. """


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    sources = [spawn, exit_node] + relics
    return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    distance = {node: float('inf') for node in graph}
    distance[source] = 0
    priority_q = [(0,source)]

    while priority_q:
        dist, curr = heapq.heappop(priority_q)

        #skip if better path found
        if dist > distance[curr]:
            continue

        if curr in graph:
            for next, weight in graph[curr]:
                if distance[curr] + weight < distance[next]:
                    distance[next] = distance[curr] + weight
                    heapq.heappush(priority_q,(distance[next],next))
    return distance


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    sources = select_sources(spawn,relics,exit_node)
    distance_tbl = {}

    for source in sources:
        distance_tbl[source] = run_dijkstra(graph, source)
        
    return distance_tbl


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """


    return """### Part 3a: What the Invariant Means

- **For nodes already finalized (in S):**
  A finalized node's distance is the true shortest path from the sources.

- **For nodes not yet finalized (not in S):**
  The value of a not finalized node is the cheapest path which torchbearer has already discovered which only uses finalized nodes as its intermediate stops. 

### Part 3b: Why Each Phase Holds

- **Initialization : why the invariant holds before iteration 1:**
  All sources start with distance = 0. All other nodes have value = \infty 

- **Maintenance : why finalizing the min-dist node is always correct:**
  Non-negative edge weights guarantee that no future path through other nodes may be shorter once a node is finalized. Therefore the finalized distance of each node is optimized.

- **Termination : what the invariant guarantees when the algorithm ends:**
  The invariant guarantees that all reachable nodes are finalized with shortest path distances from the sources, which guarantess that the distance table is accurate for all future routing decisions.

### Part 3c: Why This Matters for the Route Planner

Finding the guaranteed shortest path distances means that torchbearer will evaluate the true cost of all relic visting orders ensuring the final optimal route unmarred by inaccurate intermediate costs. """

# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    TODO
    """
    return """### Why Greedy Fails

- **The failure mode:** A greedy torchbearer picks the closest relic, but does not consider that the closest relic has after it a path that will incur a much greater cost that some marginally more expensive path now. 
- **Counter-example setup:** Consider a 2 relic setup, relics = {A,B} and then and start and exit node. with values dict {(start,A),1),(start,B),3),(A,B),10),(B,A),3),((A,end),2),((B,end),4)} and a table:
| from/to | A | B  | End |
| Start   | 1 | 3  | x   |
|   A     | x | 10 | 2   | 
|   B     | 3 | x  | 4   |

- **What greedy picks:** Start->A->B->End cost = 15
- **What optimal picks:** Start->B->A->End cost = 8
- **Why greedy loses:** Greedy is almost double (!!) the cost of the optimal selection. Choosing A first locks Torchbearer into a very expensive 10 fuel cost path to reach B. 

### What the Algorithm Must Explore

- Torchbearer's algorithm has to exhaustively explore all the possible **orders** of relics to be visted in order to guarantee finding the minimum-cost, optimal, route."""


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    if not relics:
        #no relics/relics empty, poor torchbearer just go from start to exit and calls it a day
        cost = dist_table[spawn].get(exit_node,float('inf'))
        return (cost,[])

    #initialize best with a 'NULL' or inf value and an empty list to insert jun...I mean relics into
    best = [float('inf'), []] 

    remaining_relix = relics
    _explore(dist_table,
             spawn,
             remaining_relix,
             [],
             0,
             exit_node,
             best)

    if best[0] == float('inf'):
        return (float('inf'),[])
    return (best[0],best[1])

def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    #base case: torchbearer goto exit after visiting all relics. 
    if not relics_remaining:
        total_cost = cost_so_far + dist_table[current_loc].get(exit_node, float('inf'))
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = relics_visited_order[:]
        return
    
    #determine minimum cost to finish in this current 
    low_bound = 0
    for relic in relics_remaining:
        min_cost = dist_table[current_loc].get(relic,float('inf'))
        low_bound += min_cost
    low_bound += dist_table(current_loc).get(exit_node, float('int'))

    #pruning if current branch >= best[0]
    if cost_so_far + low_bound >= best[0]:
        return
    
    #recursion, my love: traverse the tree and find the relics GO!GO!GO!
    for next in relics_remaining:
        next_cost = dist_table[current_loc].get(next, float('inf'))

        #if \exist Path -> _explore(TM)
        if next_cost != float('inf'):
            relics_remaining.remove(next)
            relics_visited_order.add(next)

            _explore(dist_table,
                     next,
                     relics_remaining,
                     relics_visited_order,
                     cost_so_far + next_cost,
                     exit_node,
                     best)
            
            relics_visited_order.pop()
            relics_remaining.add(next)

# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    
    """
    #pre-compute distances returns a dictionary distance_tbl which has run dijksra
    #on each node. no reason to copy it twice. 
    return find_optimal_route(precompute_distances(graph,spawn,relics,exit_node),
                              spawn,
                              relics,
                              exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
