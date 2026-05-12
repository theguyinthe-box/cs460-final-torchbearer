# Development Log – The Torchbearer

**Student Name:** David Kaauwai
**Student ID:** 826497939

---

## Entry 1 – May 10, 2026, 6:45pm: Initial Plan

I will implement this project in two phases: 

Phase 1: Dijkstra precomputation to build a distance table between all critical nodes (spawn, exit, relics).

Phase 2: branch-and-bound search to find the optimal relic visitation order. 

I expect Phase 1 to be a straightforward implementation of dijkstras algo, and I expect Phase 2 (pruning with lower bounds) will present a greater challenge. 

I will test Dijkstra independently on a small graph first, then validate full solution against provided test cases.

---

## Entry 2 – May 10, 2026, 10:56: Dijkstra completed and tested

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

Completed Phase one and all readmes for phase one. Completed devlog for nights work.
No bugs so far! dijstra does the thing with current tests. 
had dinner during time and pushed after I got back, not great practice, 
but I had garlic naan calling my name like a siren. 

---

## Entry 3 – May 11, 2026 8:00pm: Began Phase 2 and full testing

Implement phase 2.

  File "/media/theguyinthe_box/Syncthing/Sync/2026-SPRING/CS460-Final/SP26FinalExam460/torchbearer.py", line 272, in _explore
    low_bound += dist_table(current_loc).get(exit_node, float('int'))
                 ~~~~~~~~~~^^^^^^^^^^^^^
TypeError: 'dict' object is not callable
Fix : brackets, not parentheses

  File "/media/theguyinthe_box/Syncthing/Sync/2026-SPRING/CS460-Final/SP26FinalExam460/torchbearer.py", line 273, in _explore
    low_bound += dist_table[current_loc].get(exit_node, float('int'))
                                                        ~~~~~^^^^^^^
ValueError: could not convert string to float: 'int'
fix: inf not int

  File "/media/theguyinthe_box/Syncthing/Sync/2026-SPRING/CS460-Final/SP26FinalExam460/torchbearer.py", line 286, in _explore
    relics_visited_order.add(next)
    ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'list' object has no attribute 'add'

fix: replace add with append

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | ~45 |
| Part 2: Precomputation Design | ~90 |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | ~60(May 10) + |
| **Total** | |
