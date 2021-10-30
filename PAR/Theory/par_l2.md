# Plan generation and Classical Planning 

## What is a Plan? 

* Sequence of Instantiated Actions 
* Partial Order of Instantiated Actions Set of Instantiated Actions 
* Policy - Mapping from states to action 

## Finding a Plan 

**Searching for plans** 

* Forward Search The basic idea is to apply standard search algorithms (e.g. bread-first, depthfirst, A*, etc) to the planning problem. 
* search space is a subset of the state space nodes correspond to world states arcs correspond to state transitions path in the search space corresponds to plan 
* Backtracking Search Through a Search Space 
  * How to conduct the search 
  * How to represent the search space 
  * How to evaluate the solutions 
* Non-Deterministic Choice Points Determine Backtracking 
  * Choice of actions 
  * Choice of variable bindings 
  * Choice of temporal orderings 
  * Choice of subgoals to work on 

There are three main algorithmic techniques for solving constraint satisfaction problems (CSP) (e.g., Find plans): backtracking search, local search, and dynamic programming. 

* backtracking search algorithms work on only one solution at a time and thus need only a polynomial amount of space 
* The drawbacks of dynamic programming approaches are that they often require an exponential amount of time and space, and they do unnecessary work by finding, or making it possible to easily generate, all solutions to a CSP 

**Non-deterministic algorithms** 

A nondeterministic algorithm is which can specify, at certain points in the algorithm (called "choice points"), 

## Properties of Planning Algorithms 

* Soundness 
  * A planning algorithm is sound if all solutions are legal plans 
    * All preconditions, goals and any additional constraints are satisfied 
* Completeness 
  * A planning algorithm is complete if a solution can be found whenever one actually exists. In other words if it guarantees to return answer for any arbitrary input 
  * A planning algorithm is strictly complete if all solutions are included in the search space
* Optimality 
  * A planning algorithm is optimal if it maximizes a predefined measure of plan quality 

## Linear Planning 

Work on one goal until completely solved before moving to the next goal. 

Search by reducing the difference between the state and the goals 

The approximation of a solution of any problem is a linear solution. 

Means-Ends reasoning 

* Means-end reasoning is concerned with finding the means for achieving goals. (actions = means, goals = ends). 
* The basic idea is a simple one: to achieve a goal, we consider an action that would achieve it under some specified circumstances and then try to find a way of putting ourselves in those circumstances in order to achieve the goal by performing the action. 
* Putting ourselves in those circumstances becomes a subgoal. The idea is to work backward from the goal through subgoals until we arrive at subgoals that are already achieved. 
* The resulting sequence of actions constitutes a plan for achieving the goal. 
* A precise logical theory of plan-construction is formulated that completely characterizes means-end reasoning. 

In resume: Means-ends analysis identify and reduce, as soon as possible, differences between state and goals 

GPS => General Problem Solver 

**Advantages** 

* Reduced search space, since goals are solved one at a time, and not all possible goal orderings are considered 
* Advantageous if goals are (mainly) independent 
* Linear planning is sound 

**Disadvantages** 

* Linear planning may produce suboptimal solutions 
* Planner's efficiency is sensitive to goal orderings 
  * Control knowledge for the “right” ordering 
  * Random restarts 
  * Iterative deepening 

## NonLinear Planning 

Used to a goal set instead of a goal stack and It is included in the search space of all possible subgoal orderings. 

**Advantage** 

May be an optimal solution with respect to plan length (depending on search strategy used) 

**Disadvantages** 

* It takes larger search space, since all possible goal orderings are taken into consideration 
* Complex algorithm to understand 

## Prodigy Planner 

Extension to GPS 

* Set of goals instead of stack of goals 
* Means-ends analysis for selection of "pending goals" 
* Choice point for applying an operator when applicable and continue backward-chaining (subgoaling) 

Is able to : 

* Learn control rules 
* Conduct experiments to acquire new knowledge 

## Why is Planning Hard 

Planning involves a complex search: 

* Alternative operators to achieve a goal 
* Multiple goals that interact 
* Solution optimality , quality 
* Planning efficiency, soundness, completeness 

State Representation 

* The frame problem 
* The "choice" of predicates 

Action representation 

* Many alternative definitions 
* Conditional effects 
* Quantification 
* Functions