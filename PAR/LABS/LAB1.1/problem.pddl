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