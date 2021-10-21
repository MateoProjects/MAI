(define (domain ROBOT_MOVINGTARGET)

    (:requirements
  		:strips
		:negative-preconditions
		:equality
		:typing
		:adl
		:fluents
		:action-costs	
	)

	(:types
		circulating_robot
		moving_target_ghost	
		board_coordinate_x
		board_coordinate_y
		time_consumption
		bool_value
  	)

      ; We introduce here a cost function to calculate the cost of the plan and choose the smaller one
    (:functions
        (total-cost)
    )
	
    (:predicates
    ; We define in the predicates time variables, coordinates of the board, robot in position, ghost in position
    ; moment of robot and ghost in the same place

		(present_time     ?t  - time_consumption)
		(future_time   ?t1 - time_consumption 
					 ?t2 - time_consumption)

		(used_time   ?t  - time_consumption)

		(below_x     ?xa - board_coordinate_x
			         ?xb - board_coordinate_x)
		(one_below_x ?xa - board_coordinate_x
			         ?xb - board_coordinate_x)
		(above_x     ?xa - board_coordinate_x
			         ?xb - board_coordinate_x)
		(one_above_x ?xa - board_coordinate_x
			         ?xb - board_coordinate_x)

		(below_y     ?ya - board_coordinate_y
			         ?yb - board_coordinate_y)
		(one_below_y ?ya - board_coordinate_y
			         ?yb - board_coordinate_y)
		(above_y     ?ya - board_coordinate_y
			         ?yb - board_coordinate_y)
		(one_above_y ?ya - board_coordinate_y
			         ?yb - board_coordinate_y)

		(robot_at_coordinatex ?robot - circulating_robot
			               ?x          - board_coordinate_x)
		(robot_at_coordinatey ?robot - circulating_robot
			               ?y          - board_coordinate_y)

		(ghost_at_coordinatex ?ghost - moving_target_ghost
			               ?x          - board_coordinate_x)
		(ghost_at_coordinatey ?ghost - moving_target_ghost
			               ?y          - board_coordinate_y)

		(in_the_same_place ?bool - bool_value)
		
		(robot_movement ?bool - bool_value)

		(position_ghost ?index_x - board_coordinate_x
						  ?index_y - board_coordinate_y
						  ?time    - time_consumption)
	)



	; Here we define that when the robot is moving it will get where the ghost is and in that moment the effect (in_the_same_place) 
    ; will become true
	(:action apply_same_location
		:parameters(
            ?robot    - circulating_robot
            ?ghost    - moving_target_ghost
			?first_coordinate_x  - board_coordinate_x
			?first_coordinate_y  - board_coordinate_y
        )
		:precondition(
            and
            (robot_movement)
            (robot_at_coordinatex ?robot ?first_coordinate_x)
            (ghost_at_coordinatex ?ghost ?first_coordinate_x)
            (robot_at_coordinatey ?robot ?first_coordinate_y)
            (ghost_at_coordinatey ?ghost ?first_coordinate_y)	
        )
		:effect(
            and
            (in_the_same_place)
        )
	)
    ; the following actions are based on the robot movement through the space in the board 
	; (This first action defines the robot movement to the left)
	(:action move_robot_left
		:parameters(
            ?robot      - circulating_robot
			?first_coordinate_x - board_coordinate_x
			?destination_coordinate_x  - board_coordinate_x
        )
		:precondition(
            and
            (robot_movement true)
		(not(robot_at_coordinatex ?robot      ?destination_coordinate_x))
            (robot_at_coordinatex ?robot      ?first_coordinate_x)
            (one_above_x       ?first_coordinate_x ?destination_coordinate_x)
        )
		:effect(
            and
			(increase (total-cost) 1)
            (not (robot_movement true))
            (not (robot_at_coordinatex ?robot      ?first_coordinate_x))
            (     robot_at_coordinatex ?robot      ?destination_coordinate_x)
        )
	)
    ; (This second action defines the robot movement to the right)
	(:action move_robot_right
		:parameters(
            ?robot      - circulating_robot
			?first_coordinate_x - board_coordinate_x
			?destination_coordinate_x  - board_coordinate_x
        )
		:precondition(
            and
            (robot_movement true)
		(not(robot_at_coordinatex ?robot      ?destination_coordinate_x))
            (robot_at_coordinatex ?robot      ?first_coordinate_x)
            (one_below_x       ?first_coordinate_x ?destination_coordinate_x)
        )
		:effect(
            and
			(increase (total-cost) 1)
            (not (robot_movement true))
            (not (robot_at_coordinatex ?robot      ?first_coordinate_x))
            (     robot_at_coordinatex ?robot      ?destination_coordinate_x)
        )
	)
    
    ; (This third action defines the robot movement down to the board)
	(:action move_robot_down
		:parameters(
            ?robot      - circulating_robot
			?first_coordinate_y - board_coordinate_y
			?destination_coordinate_y  - board_coordinate_y
        )
		:precondition(
            and
            (robot_movement true)
		(not(robot_at_coordinatey ?robot      ?destination_coordinate_y))
            (robot_at_coordinatey ?robot      ?first_coordinate_y)
            (one_below_y       ?first_coordinate_y ?destination_coordinate_y)
        )
		:effect(
            and
			(increase (total-cost) 1)
            (not (robot_movement true))
            (not (robot_at_coordinatey ?robot      ?first_coordinate_y))
            (     robot_at_coordinatey ?robot      ?destination_coordinate_y)
        )
	)

; (This fourth action defines the robot movement up to the board)
	(:action move_robot_up
		:parameters(
            ?robot      - circulating_robot
			?first_coordinate_y - board_coordinate_y
			?destination_coordinate_y  - board_coordinate_y
        )
		:precondition(
            and
            (robot_movement true)
		(not(robot_at_coordinatey ?robot      ?destination_coordinate_y))
            (robot_at_coordinatey ?robot      ?first_coordinate_y)
            (one_above_y       ?first_coordinate_y ?destination_coordinate_y)
        )
		:effect(
            and
			(increase (total-cost) 1)
            (not (robot_movement true))
            (not (robot_at_coordinatey ?robot      ?first_coordinate_y))
            (     robot_at_coordinatey ?robot      ?destination_coordinate_y)
        )
	)
	
	; Here we define the ghost movements: moving to predefined positions in the board.
	; This action just stablishes the ghost moving to a certain position 
	(:action ghost_moves_to_predefined_location
		:parameters(
            ?ghost - moving_target_ghost

			?present_moment    - time_consumption
			?first_coordinate_x - board_coordinate_x
			?first_coordinate_y - board_coordinate_y

			?ahead_moment     - time_consumption
			?next_coordinate_x  - board_coordinate_x
			?next_coordinate_y  - board_coordinate_y
        )
		:precondition(
            and
            (not ( robot_movement true ))
			(      present_time ?present_moment )
			(not ( present_time ?ahead_moment  ))
			(      ghost_at_coordinatex ?ghost ?first_coordinate_x )
			(      ghost_at_coordinatey ?ghost ?first_coordinate_y )
			(      position_ghost ?next_coordinate_x  ?next_coordinate_y  ?ahead_moment)
			(      future_time        ?present_moment    ?ahead_moment)

        )
		:effect(
            and
            (robot_movement true)
			(not ( present_time ?present_moment ))
			(      present_time ?ahead_moment  )
			(not ( ghost_at_coordinatex ?ghost ?first_coordinate_x ))
			(not ( ghost_at_coordinatey ?ghost ?first_coordinate_y ))
			(      ghost_at_coordinatex ?ghost ?next_coordinate_x  )
			(      ghost_at_coordinatey ?ghost ?next_coordinate_y  )
			(      used_time ?present_moment )
        )
	)

	; When in the planing of the problem there are no more positions for the ghost, the ghost remains.
    ; It is important to remember that the ghost in this case, is the moving target (specified above).
	(:action ghost_stays
		:parameters(
            ?ghost      - moving_target_ghost

			?present_moment    - time_consumption
			?first_coordinate_x - board_coordinate_x
			?first_coordinate_y - board_coordinate_y

			?ahead_moment     - time_consumption
			?next_coordinate_x  - board_coordinate_x
			?next_coordinate_y  - board_coordinate_y
        )
		:precondition(
            and
            (not ( robot_movement true))
			(      present_time ?present_moment )
			(not ( present_time ?ahead_moment  ))
			(      future_time ?present_moment ?ahead_moment)

			(      ghost_at_coordinatex ?ghost ?first_coordinate_x )
			(      ghost_at_coordinatey ?ghost ?first_coordinate_y )
			
			(not ( used_time ?present_moment ))
        )
		:effect(
            and
            (robot_movement true)
			(not ( present_time ?present_moment ))
			(      present_time ?ahead_moment  )

        )
	)



)
