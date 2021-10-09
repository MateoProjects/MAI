(define (domain lunar-middle)
    (:requirements :strips :typing :adl)
    (:types spacecraft - object
            position - object)
    
    (:predicates
        (middle-of ?p1 ?p2 ?p3 - position) ; p1 < p2 < p3
        (next-of ?p1 ?p2 - position) ; p1 + 1 = p2 
        (pos ?s - spacecraft ?x1 ?y1 - position)
    )
    
    (:action move_up
        :parameters 
        (   
            ?spacecraft ?stop_craft - spacecraft 
            ?x ?old_y ?new_y ?stop_y - position
        )
        :precondition
            (and
                (pos ?spacecraft ?x ?old_y)
                (pos ?stop_craft ?x ?stop_y)
                (next-of ?new_y ?stop_y)
                (middle-of ?old_y ?new_y ?stop_y)
                (forall (?s - spacecraft ?y - position)
                    (not (and (pos ?s ?x ?y) (middle-of ?old_y ?y ?stop_y)))
                )
            )
        :effect
            (and 
                (not (pos ?spacecraft ?x ?old_y))
                (pos ?spacecraft ?x ?new_y)
            )
    )
    
    (:action move_down
        :parameters    
        (
            ?spacecraft ?stop_craft - spacecraft 
            ?x ?old_y ?new_y ?stop_y - position
        )
        :precondition
            (and
                (pos ?spacecraft ?x ?old_y)
                (pos ?stop_craft ?x ?stop_y)
                (next-of ?stop_y ?new_y)
                (middle-of ?stop_y ?new_y ?old_y)
                (forall (?s - spacecraft ?y - position)
                    (not (and (pos ?s ?x ?y) (middle-of ?stop_y ?y ?old_y)))
                )
            )
        :effect
            (and 
                (not (pos ?spacecraft ?x ?old_y))
                (pos ?spacecraft ?x ?new_y)
            )
    )
    
    (:action move_right
        :parameters  
        (
            ?spacecraft ?stop_craft - spacecraft 
            ?y ?old_x ?new_x ?stop_x - position
        )
        :precondition
            (and
                (pos ?spacecraft ?old_x ?y)
                (pos ?stop_craft ?stop_x ?y)
                (next-of ?new_x ?stop_x)
                (middle-of ?old_x ?new_x ?stop_x)
                (forall (?s - spacecraft ?x - position)
                    (not (and (pos ?s ?x ?y) (middle-of ?old_x ?x ?stop_x)))
                )
            )
        :effect
            (and 
                (not (pos ?spacecraft ?old_x ?y))
                (pos ?spacecraft ?new_x ?y)
            )
    )
    
    (:action move_left
        :parameters    
        (
            ?spacecraft ?stop_craft - spacecraft 
            ?y ?old_x ?new_x ?stop_x - position
        )
        :precondition
            (and
                (pos ?spacecraft ?old_x ?y)
                (pos ?stop_craft ?stop_x ?y)
                (next-of ?stop_x ?new_x)
                (middle-of ?stop_x ?new_x ?old_x)
                (forall (?s - spacecraft ?x - position)
                    (not (and (pos ?s ?x ?y) (middle-of ?stop_x ?x ?old_x)))
                )
            )
        :effect
            (and 
                (not (pos ?spacecraft ?old_x ?y))
                (pos ?spacecraft ?new_x ?y)
            )
    )
)
    