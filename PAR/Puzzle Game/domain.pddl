;Header and description

(define (domain puzzlegame)

;remove requirements that are not needed
(:requirements :strips :fluents :durative-actions :timed-initial-literals :typing :conditional-effects :negative-preconditions :duration-inequalities :equality)

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    board_coordinate_x
    board_coordinate_y
    value
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    (below_x     ?xa - board_coordinate_x
                 ?xb - board_coordinate_x)
    (above_x     ?xa - board_coordinate_x
                 ?xb - board_coordinate_x)
    (below_y     ?ya - board_coordinate_y
                 ?yb - board_coordinate_y)
    (above_y     ?ya - board_coordinate_y
                 ?yb - board_coordinate_y)

    (atCell ?xa-board_coordinate_x ?ya-board_coordinate_y ?val - value) ; check if white is in coord x
    (whereWhite ?xa-board_coordinate_x ?ya-board_coordinate_y ?white - value) ; check if white is in coord
    
    )


(:functions ;todo: define numeric functions here
)

;define actions here
(:action move_left
    :parameters (
        ?xa - board_coordinate_x
        ?ya - board_coordinate_y
        ?xb - board_coordinate_x
        ?yb - board_coordinate_y
        ?val - value
        ?white - white
    )
    :precondition (and 
        (atCell ?xa ?ya ?val)
        (whereWhite ?xb ?yb ?white)
        (above_x ?xa ?xb)
    
    )
    :effect (and (whereWhite ?xa ?ya ?white)(not(whereWhite ?xb ?yb ?white)) (atCell ?xb ?yb ?val) (not(atCell ?xa ?ya ?val)))
)
; fins aqui fet
(:action move_right
    :parameters (
        ?xa - board_coordinate_x
        ?ya - board_coordinate_y
        ?xb - board_coordinate_x
        ?yb - board_coordinate_y
        ?val - value
        ?white - value
    )
    :precondition (and 
        (atCell ?xa ?ya ?val)
        (whereWhite ?xb ?yb ?white)
        (below_x ?xa ?xb)
    )
        :effect (and (whereWhite ?xa ?ya ?white)(not(whereWhite ?xb ?yb ?white)) 
        (atCell ?xb ?yb ?val) (not(atCell ?xa ?ya ?val)))

)

(:action move_up
    :parameters (
        ?xa - board_coordinate_x
        ?ya - board_coordinate_y
        ?xb - board_coordinate_x
        ?yb - board_coordinate_y
        ?val - value
        ?white - value
    )
    :precondition (and 
        (atCell ?xa ?ya ?val)
        (whereWhite ?xb ?yb ?white )
        (above_y ?ya ?yb)
    )
    :effect (and (whereWhite ?xa ?ya ?white)(not(whereWhite ?xb ?yb ?white))
     (atCell ?xb ?yb ?val) (not(atCell ?xa ?ya ?val)))
)

(:action move_down
    :parameters (
        ?xa - board_coordinate_x
        ?ya - board_coordinate_y
        ?xb - board_coordinate_x
        ?yb - board_coordinate_y
        ?val - value
        ?white - value
    )
    :precondition (and 
        (atCell ?xa ?ya ?val)
        (where ?xb ?yb ?white )
        (below_y ?ya ?yb)
    )
    :effect (and (whereWhite ?xa ?ya ?white)(not(whereWhite ?xb ?yb ?white)) (atCell ?xb ?yb ?val) (not(atCell ?xa ?ya ?val)))
)





)