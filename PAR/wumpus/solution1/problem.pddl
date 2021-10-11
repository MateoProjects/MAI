(define (problem wumpus-prob)
    (:domain wumpus1)
    (:objects
        sq-1-1 - room
        sq-1-2 - room
        sq-1-3 - room
        sq-2-1 - room
        sq-2-2 - room
        sq-2-3 - room
        agent - who
    )

    (:init
        (adj sq-1-1 sq-1-2)
        (adj sq-1-2 sq-1-1)
        (adj sq-1-2 sq-1-3)
        (adj sq-1-3 sq-1-2)
        (adj sq-2-1 sq-2-2)
        (adj sq-2-2 sq-2-1)
        (adj sq-2-2 sq-2-3)
        (adj sq-2-3 sq-2-2)
        (adj sq-1-1 sq-2-1)
        (adj sq-2-1 sq-1-1)
        (adj sq-1-2 sq-2-2)
        (adj sq-2-2 sq-1-2)
        (adj sq-1-3 sq-2-3)
        (adj sq-2-3 sq-1-3)
        (pit sq-1-2)
        (not (havegold agent))
        (wump sq-2-3)
        (agnt sq-1-1)
        (havearow agent)
        (gld sq-1-3)
        ; a p g
        ; x x w
    )

    (:goal
        (and (agnt sq-2-2) (havegold agent)
        )
    )

  
)