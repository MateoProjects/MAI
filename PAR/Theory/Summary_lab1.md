# Introduction to PDDL files

**We need to define first of all two diferent files.**


1. **domain.pddl** : In this file we define the domain of our Agent.  First of all we define the domain, next requiremenets and predicates and finally we need to define all actions that our agent can do.  

* **Exemple**

```pddl
(define (domain blocksworld)
    (:requirements :strips :equality)
    (:predicates
        (clear ?x)
        (on-table ?x)
        (arm-empty)
        (holding ?x)
        (on ?x ?y)
    )
    (:action pickup
        :parameters (?ob)
        :precondition (and (clear ?ob) (on-table ?ob) (arm-empty))
        :effect (and (holding ?ob) (not (clear ?ob)) (not (on-table ?ob))
            (not (arm-empty)))
    )
```

2. **problem.pddl** : In this file we define the problem that our agent will be try to solve. We need to define the objects that we have on this problem, the init state and the Goal. 

```pddl
(define (problem pb1)
    (:domain blocksworld)
    (:objects
        a b c d
    )
    (:init
        (on-table a)
        (on-table b)
        (on-table c)
        (on d c)
        (clear a)
        (clear b)
        (clear d)
        (arm-empty)
    )
    (:goal
        (and (on a b) (on b d) (on-table c) (clear c))
    )
)

```
