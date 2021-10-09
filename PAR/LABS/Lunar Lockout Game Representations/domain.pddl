(define (domain lunarlockoutdynamic)
  (:requirements :strips :adl :typing :fluents)
  (:types
    position - object
    spacecraft - object
  )
  (:predicates
    (just_left_of ?l - position ?r - position) ; position l is left of position r, exactly next to it
    (just_above_of ?u - position ?d - position) ; position u is above of position d, exactly next to it
    (empty ?p - position)
    (at ?sp -spacecraft ?pos - position) ; spacecraft at position
    (movingup ?sp - spacecraft)
    (movingleft ?sp - spacecraft)
    (movingdown ?sp - spacecraft)
    (movingright ?sp - spacecraft)
    (static)
  )
  (:functions
    (moves)
  )
  ; Each direction has 3 separate actions, one to start moving a spacecraft, one for moving it and one for stopping to move it.
  ; Starting movement is only allowed when no spacecraft is moving, AKA: board is static.
  ; Moving is only allowed when the spacecraft is moving in that direction AND the next spot is empty
  ; Stopping to move is only allowed when the spacecraft is moving in that direction AND the next spot is NOT empty
  ;
  ; To emulate the edges of the board, we set extra positions which are not empty: thus they can stop the movement.
  (:action startmoveup
    :parameters (?sp - spacecraft)
    :precondition (static)
    :effect (and 
              (movingup ?sp)
              (not (static))
              (increase (moves) 1)
            )
  )
  (:action moveup
    :parameters (?sp - spacecraft ?ini - position ?fi - position)
    :precondition (and 
              (movingup ?sp)
              (at ?sp ?ini)
              (just_above_of ?fi ?ini)
              (empty ?fi)
            )
    :effect (and 
              (empty ?ini)
              (not (at ?sp ?ini))
              (not (empty ?fi))
              (at ?sp ?fi)
            )
  )
  (:action stopmoveup
    :parameters (?sp - spacecraft ?ini - position ?lim - position)
    :precondition (and 
              (movingup ?sp)
              (at ?sp ?ini)
              (just_above_of ?lim ?ini)
              (not(empty ?lim))
            )
    :effect (and 
              (not (movingup ?sp))
              (static)
            )
  )
  ;
  (:action startmovedown
    :parameters (?sp - spacecraft)
    :precondition (static)
    :effect (and 
              (movingdown ?sp)
              (not (static))
              (increase (moves) 1)
            )
  )
  (:action movedown
    :parameters (?sp - spacecraft ?ini - position ?fi - position)
    :precondition (and 
              (movingdown ?sp)
              (at ?sp ?ini)
              (just_above_of ?ini ?fi)
              (empty ?fi)
            )
    :effect (and 
              (empty ?ini)
              (not (at ?sp ?ini))
              (not (empty ?fi))
              (at ?sp ?fi)
            )
  )
  (:action stopmovedown
    :parameters (?sp - spacecraft ?ini - position ?lim - position)
    :precondition (and 
              (movingdown ?sp)
              (at ?sp ?ini)
              (just_above_of ?ini ?lim)
              (not(empty ?lim))
            )
    :effect (and 
              (not (movingdown ?sp))
              (static)
            )
  )
  ;
  (:action startmoveleft
    :parameters (?sp - spacecraft)
    :precondition (static)
    :effect (and 
              (movingleft ?sp)
              (not (static))
              (increase (moves) 1)
            )
  )
  (:action moveleft
    :parameters (?sp - spacecraft ?ini - position ?fi - position)
    :precondition (and 
              (movingleft ?sp)
              (at ?sp ?ini)
              (just_left_of ?fi ?ini)
              (empty ?fi)
            )
    :effect (and 
              (empty ?ini)
              (not (at ?sp ?ini))
              (not (empty ?fi))
              (at ?sp ?fi)
            )
  )
  (:action stopmoveleft
    :parameters (?sp - spacecraft ?ini - position ?lim - position)
    :precondition (and 
              (movingleft ?sp)
              (at ?sp ?ini)
              (just_left_of ?lim ?ini)
              (not(empty ?lim))
            )
    :effect (and 
              (not (movingleft ?sp))
              (static)
            )
  )
  ;
  (:action startmoveright
    :parameters (?sp - spacecraft)
    :precondition (static)
    :effect (and 
              (movingright ?sp)
              (not (static))
              (increase (moves) 1)
            )
  )
  (:action moveright
    :parameters (?sp - spacecraft ?ini - position ?fi - position)
    :precondition (and 
              (movingright ?sp)
              (at ?sp ?ini)
              (just_left_of ?ini ?fi)
              (empty ?fi)
            )
    :effect (and 
              (empty ?ini)
              (not (at ?sp ?ini))
              (not (empty ?fi))
              (at ?sp ?fi)
            )
  )
  (:action stopmoveright
    :parameters (?sp - spacecraft ?ini - position ?lim - position)
    :precondition (and 
              (movingright ?sp)
              (at ?sp ?ini)
              (just_left_of ?ini ?lim)
              (not(empty ?lim))
            )
    :effect (and 
              (not (movingright ?sp))
              (static)
            )
  )
)