(define (problem pb1)
    (:domain blocksworld)
    (:objects
        a b c
    )
    (:init
        (on-table a)
        (on-table b)
        (on-table c)
        (clear a)
        (clear b)
        (clear c)
        (arm-empty)
    )
    (:goal
        (and (on a b) (on b c))
    )
)