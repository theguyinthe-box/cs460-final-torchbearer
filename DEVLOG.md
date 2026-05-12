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

  File "./SP26FinalExam460/torchbearer.py", line 272, in _explore
    low_bound += dist_table(current_loc).get(exit_node, float('int'))
                 ~~~~~~~~~~^^^^^^^^^^^^^
TypeError: 'dict' object is not callable
Fix : brackets, not parentheses

  File "./SP26FinalExam460/torchbearer.py", line 273, in _explore
    low_bound += dist_table[current_loc].get(exit_node, float('int'))
                                                        ~~~~~^^^^^^^
ValueError: could not convert string to float: 'int'
fix: inf not int

  File "./SP26FinalExam460/torchbearer.py", line 286, in _explore
    relics_visited_order.add(next)
    ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'list' object has no attribute 'add'

  File "./SP26FinalExam460/torchbearer.py", line 297, in _explore
    relics_remaining.add(next)
    ^^^^^^^^^^^^^^^^^^^^
AttributeError: 'list' object has no attribute 'add'

fix: replace add with append

Traceback (most recent call last):
  File "/media/theguyinthe_box/Syncthing/Sync/2026-SPRING/CS460-Final/SP26FinalExam460/torchbearer.py", line 391, in <module>
    _run_tests()
    ~~~~~~~~~~^^
  File "/media/theguyinthe_box/Syncthing/Sync/2026-SPRING/CS460-Final/SP26FinalExam460/torchbearer.py", line 343, in _run_tests
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
           ^^^^^^^^^
AssertionError: Test 1 FAILED: expected 4, got 6

table for test 1

f\t | B | C | D | T |
|---|---|---|---|---|
| S | 1 | 2 | 2 | x |
| B | x | x | 1 | 1 |
| C | 1 | x | x | 1 |
| D | 1 | 1 | x | x | 

Three possible paths:
S->B->D->C->T = 4
S->D->C->B->T = 5
S->D->B->C->T = 5

after running debugger, realized algorithm is running over paths that don't even exist. eg: S->C->B->D->T = not possible no exit on D should be pruning.


---

## Entry 4 – May 12 2:15am: Post-Implementation Reflection

consdidering all current tests have been passed, I'd most change going to bed at a reasonable hour. 

I'll turn this in in the morning after one last look over for completeness, but I think this biggest thing I would do additionally would be the development of more edge case tests. and more complicated tests that would push the limits of the algo and provide some empirical evidence of the theoretical optimality. 

Anyway, it was a fun assignment. neat to think about. maybe consider A* and dijkstra's comparison in a future class since both with branch and bounding. A* should do better, but you gotta introduce heuristics which I understand might be outside the scope of the class.
---

## Final Entry – May 12 2:26am: Time Estimate


| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | ~45 |
| Part 2: Precomputation Design | ~90 |
| Part 3: Algorithm Correctness | ~30 |
| Part 4: Search Design | ~45 |
| Part 5: State and Search Space | ~60 |
| Part 6: Pruning | ~20 |
| Part 7: Implementation | lost track |
| README and DEVLOG writing | ~60(May 10) + lost track | %aren't the above in the README. idk what you want. 
| **Total** | a heckin lot |
