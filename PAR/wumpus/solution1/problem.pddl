(define (problem wumpus-p)
    (:domain wumpus-a)
    (:objects
        sq-1-1 sq-1-2 sq-1-3 sq-2-1 sq-2-2 sq-2-3 agent wumpus arrow gold pit
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

        (at gold sq-1-3)
        (at agent sq-1-1)
        (have agent arrow)
        (at wumpus sq-2-3)
        ;todo: put the initial state's facts and numeric values here
    )

    (:goal
        (and (have agent gold) (at agent sq-1-1)
            ;todo: put the goal condition here
        )
    )

    ;un-comment the following line if metric is needed
    ;(:metric minimize (???))
)