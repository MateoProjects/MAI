# PDDL - The Planning Domain Denition Language

---

## Types of requirements 

```PDDL
:strips Basic STRIPS-style adds and deletes 

:typing Allow type names in declarations of variables 

:disjunctive-preconditions Allow or in goal descriptions 

:equality Support = as built-in predicate :existential-preconditions Allow exists in goal descriptions 

:universal-preconditions Allow forall in goal descriptions 

:quantified-preconditions = :existential-preconditions + :universal-preconditions 

:conditional-effects Allow when in action effects 

:action-expansions Allow actions to have :expansions 

:foreach-expansions Allow actions expansions to use foreach (implies :action-expansions) 

:dag-expansions Allow labeled subactions (implies :action-expansions) 

:domain-axioms Allow domains to have :axioms 

:subgoal-through-axioms Given axioms p q and goal q, generate subgoal p 

:safety-constraints Allow :safety conditions for a domain 

:expression-evaluation Support eval predicate in axioms (implies :domain-axioms) 

:fluents Support type (fluent t). Implies :expression-evaluation 

:open-world Don't make the \closed-world assumption" for all predicates | i.e., if an atomic formula is not known to be true, it is not necessarily assumed false 

:true-negation Don't handle not using negation as failure, but treat it as in rst-order logic (implies :open-world) 

:adl = :strips + :typing + :disjunctive-preconditions + :equality + :quantified-preconditions + :conditional-effects 

:ucpop = :adl + :domain-axioms + :safety-constraints
```

## Variables

the symbols starting with question marks denote variables

```
?m , ?n 
```

## Predicates

```
(:predicates
    (<predicate_name> <argument_1> ... <argument_n>)
)
```

Predicates apply to a specific type of object, or to all objects. Predicates are either true or false at any point in a plan and when not declared are assumed to be false (except when the Open World Assumption is included as a requirement).

## Actions

```PDDL
(:action <action_name>
    :parameters (<argument_1> ... <argument_n>)
    :precondition (<logical_expression>)
    :effect (<logical_expression>)
    ; :expansion
)
```

An action defines a transformation the state of the world. This transformation is typically an action which could be performed in the execution of the plan, such as picking up an object, constructing something or some other change.

* **parameters**: section which defines the things we are performing an action on and subsequently what predicates we will be checking and manipulating later.
* **precondition**: These are typically a series of predicate conjunctions and disjunctions which must be satisfied in order for the action the applied

**Exemple**

```
(:action BUILD-WALL
    :parameters (?s - site ?b - bricks)
    :precondition (and
        (on-site ?b ?s)
        (foundations-set ?s)
        (not (walls-built ?s))
        (not (material-used ?b))
    )
    :effect (and
        (walls-built ?s)
        (material-used ?b)
    )
)
```

### Preconditions

```
:precondition (and
    (on-site ?b ?s)
    (foundations-set ?s)
    (not (walls-built ?s))
    (not (material-used ?b))
)
```

Preconditions are conditions which must be met in order for an action to be possible. Just because an action is possible, does not mean that it is definitely applied and a planner will always consider if an action moves the state closer to the goal state.

* **and** : A conjunction of predicates, expressing that all values must be true in order to evaluate to true. 
* **or** : A disjunction of predicates, expressing at least one of the values must be true in order to evaluate true. 

## Effects 

The :effect describes the effects of the action

```
(:action spray-paint
    :parameters (?c - color)
    :vars (?x - location)
    :precondition (at robot ?x)
    :effect (forall (?y - physob)
        (when (at ?y ?x)
        (color ?y ?c))))
```

