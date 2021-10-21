;Header and description

(define (domain p1)

;remove requirements that are not needed
(:requirements :strips :fluents :typing :conditional-effects :negative-preconditions)

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

    (atCell ?xa - board_coordinate_x ?ya - board_coordinate_y ?val - value) ; check if white is in coord x
    (whiteIn ?xa - board_coordinate_x ?ya - board_coordinate_y)
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
    )
    :precondition (and 
        (atCell ?xa ?ya ?val)
        (whiteIn ?xb ?yb)
        (above_x ?xa ?xb)
    
    )
    :effect (and (whiteIn ?xa ?ya) (not (whiteIn ?xb ?yb)) (atCell ?xb ?yb ?val) (not (atCell ?xa ?ya ?val)))
)
; fins aqui fet
(:action move_right
    :parameters (
        ?xa - board_coordinate_x
        ?ya - board_coordinate_y
        ?xb - board_coordinate_x
        ?yb - board_coordinate_y
        ?val - value
    )
    :precondition (and 
        (atCell ?xa ?ya ?val)
        (whiteIn ?xb ?yb)
        (below_x ?xa ?xb)
    )
    :effect (and (whiteIn ?xa ?ya) (not (whiteIn ?xb ?yb)) (atCell ?xb ?yb ?val) (not (atCell ?xa ?ya ?val)))

)

(:action move_up
    :parameters (
        ?xa - board_coordinate_x
        ?ya - board_coordinate_y
        ?xb - board_coordinate_x
        ?yb - board_coordinate_y
        ?val - value
    )
    :precondition (and 
        (atCell ?xa ?ya ?val)
        (whiteIn ?xb ?yb )
        (above_y ?ya ?yb)
    )
    :effect (and (whiteIn ?xa ?ya) (not (whiteIn ?xb ?yb)) (atCell ?xb ?yb ?val) (not (atCell ?xa ?ya ?val)))

)

(:action move_down
    :parameters (
        ?xa - board_coordinate_x
        ?ya - board_coordinate_y
        ?xb - board_coordinate_x
        ?yb - board_coordinate_y
        ?val - value
    )
    :precondition (and 
        (atCell ?xa ?ya ?val)
        (whiteIn ?xb ?yb )
        (below_y ?ya ?yb)
    )
    :effect (and (whiteIn ?xa ?ya) (not (whiteIn ?xb ?yb)) (atCell ?xb ?yb ?val) (not (atCell ?xa ?ya ?val)))
)





)