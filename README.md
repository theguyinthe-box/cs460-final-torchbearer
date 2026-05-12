# The Torchbearer

**Student Name:** David Kaauwai
**Student ID:** 826497939
**Course:** CS 460 – Algorithms | Spring 2026

---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
 The shortest path or the least number of nodes visited by the torchbearer doesn't gurantee that the minimum fuel will consumed, it doesn't even guarantee that the torchbearer will not run out of fuel before it reaches the end. In other words, a single shortest path only reaches one specific node, it doesn't decide which relic to visit first to optimally reserve its fuel. 

- **What decision remains after all inter-location costs are known:**
The only decision that remains once the torchbearer knows all interlocation costs is to determine the order of the relics it'll be retrieving. 

- **Why this requires a search over orders (one sentence):**
Different permutations of the orders of relics produce different fuel costs, so computing a single path would not be guaranteed to find the route that costs the minimum fuel. 

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| spawn | starting point need shortest paths from S to all relics and exit for routing decision making |
| relics | ojectives. need shortest paths from each relic to remaining relics and exit for routing decision making |
| exit | the exit. need shortest paths from exit to verify that tourchbearer can reach the exit |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | nested dictionary dict[node,dict[node,float]|
| What the keys represent | outer key is source node, inner key is destination node. |
| What the values represent | the shortest distance from source to the next destination |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Direct key lookup in a python dict is a constant time operation. |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** k + 2 where k is the number of relic nodes plus start node and exit node. 
- **Cost per run:** O(m log n)
- **Total complexity:** O((k+2)m log n) = O(km log n)
- **Justification (one line):** Dijkstra runs from k+2 sources: spawn, exit_node, and k relic nodes. Each run processes all edges within a heap operation. 

---

## Part 3: Algorithm Correctness

### Part 3a: What the Invariant Means

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

Finding the guaranteed shortest path distances means that torchbearer will evaluate the true cost of all relic visting orders ensuring the final optimal route unmarred by inaccurate intermediate costs. 

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** A greedy torchbearer picks the closest relic, but does not consider that the closest relic has after it a path that will incur a much greater cost that some marginally more expensive path now. 
- **Counter-example setup:** Consider a 2 relic setup, relics = {A,B} and then and start and exit node. with values dict {(start,A),1),(start,B),3),(A,B),10),(B,A),3),((A,end),2),((B,end),4)} and a table:

| from/to | A | B | End |
|---|---|---|---|
| Start | 1 | 3 | x |
| A | x | 10 | 2 | 
| B | 3 | x | 4 |

- **What greedy picks:** Start->A->B->End cost = 15
- **What optimal picks:** Start->B->A->End cost = 8
- **Why greedy loses:** Greedy is almost double (!!) the cost of the optimal selection. Choosing A first locks Torchbearer into a very expensive 10 fuel cost path to reach B. 

### What the Algorithm Must Explore

- Torchbearer's algorithm has to exhaustively explore all the possible **orders** of relics to be visted in order to guarantee finding the minimum-cost, optimal, route.  
---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node | current node being consdiered by torchbearer |
| Relics already collected | relics_visited_order | list | list of finalized order of relics to visit |
| Fuel cost so far | cost_so_far | float | cost of fuel in current branching algorithm |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | BnB adds and removes relics several times dirring backtracking operations. Python SET provides O(1) operations for check/add/remove operations |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** $K!$ where $K$ is the number of relics
- **Why:** Worst case ontario, the algorithm prunes exactly zero branches and torchbearer explores every possible permutation of relic visiting orders before it actually determines the best possible route. 

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** minimum fuel cost already determined and the list of current finalized relics
- **When it is used:** when each route hits the exit-node base case with all relics visited, the total cost of the current branch is compared to current best
- **What it allows the algorithm to skip:** all partial paths where cost_so_far + low_bound is >= best. not like they can hope to beat it anyway. 

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** current location, remaining relics, and cummulative cost.
- **What the lower bound accounts for:** the sum of lowest costs from the current relic to each unvisted relic and the lowest cost from current relic to the exit.
- **Why it never overestimates:** low_bound assumes 1) that all weights are non-negative, so 0 is the least possible infimum. 2) relics can all be visited at the same time. That is impossible, but that also means that low_bound \le \forall completion cost, so it's an admissable bound. 

### Part 6c: Pruning Correctness

if cost_so_for + low_bound >= best[0], then all possible complete paths in the current branch with have cost >= best[0]. therefore the alogorithm can prune without missing the optimal solution.

---

## References

> Bullet list. If none beyond lecture notes, write that.

- https://artint.info/html1e/ArtInt_63.html
- https://docs.python.org/3/tutorial/datastructures.html (for Sets, lists, and Dicts)