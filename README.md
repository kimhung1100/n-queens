# Introduction to AI ASSIGNMENT 1
N-queens problem solver, Python 3.9.

To run it:
```bash 
python main.py
```
---

- [ ] Slide https://www.overleaf.com/3643154285cbpwnjpfqymg 
- [x]  DFS implementation

- [x] BrFS implementation

- [x] Heuristic algorithm 
 
- [x] Random restart hill climbing

- Stimulate annealing, heuristic O(N^2)
- [x] Run in 1000 queen in 276s
- [ ] Run in N queens = 100000 

3. Heuristic algorithm

Based on Martinjak, Ivica; Golub, Marin "Comparison of heuristic algorithms for the n-queen problem"

Simulated annealing is
the only algorithm that is able to solve instances
with large dimensions (500000 queens) of the
problem in a realistic time frame which is
achieved due to the reduction of the fitness
function complexity to O(1).

Also, large dimension is possible to achieve with genetic
algorithm if parallel genetic algorithm is used.

I tried Simulated annealing algorithm.

---

Implemented with divide and conquer stimulate annealing.



---
In textbook - page 132:
For 8-queens, then random-restart hill climbing is very effective indeed. Even for three million queens, the approach can find solutions in seconds.

I have implemented random-restart, ran in several small number.

If I have time, test later.

