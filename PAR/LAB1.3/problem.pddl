(define (problem pb1)
    (:domain blocksworld)
    (:objects
        a b c d e f g h
    )
    (:init
        (on-table b)
        (clear a)
        (on a h)
        (on h g)
        (on g f)
        (on f e)
        (on e d)
        (on d c)
        (on c b)
        (arm-empty)
    )
    (:goal
        (and (on h g) (on g f)(on f e)(on e d)(on d c)(on c b)(on b a)
            (on-table a) (clear h))
    )
)