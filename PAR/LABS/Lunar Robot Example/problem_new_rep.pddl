(define (problem MT_GHOST)
 
    (:domain ROBOT_MOVINGTARGET)

    (:objects
    ; Definition of our objects: board coordinates, time, bool value, robot and ghost
        X0 X1 X2 X3 X4 - board_coordinate_x
        Y0 Y1 Y2 Y3 Y4 - board_coordinate_y
        T0 T1 T2 T3 T4 T5 T6 T7 T8 T9 - time_consumption
        true false - bool_value
        robot1   - circulating_robot
        ghost1   - moving_target_ghost
    )

    (:init
        ; Definition of cost function for the start moment
        (= (total-cost) 0)


        ; Time axis description, with relative positions from T0 to T9
        (future_time T0 T1)
        (future_time T1 T2)
        (future_time T2 T3)
        (future_time T3 T4)
        (future_time T4 T5)
        (future_time T5 T6)
        (future_time T6 T7)
        (future_time T7 T8)
        (future_time T8 T9)
        
        ; Board configuration below
        ; Description of the how are distributed the X coordinates in the board
        (one_below_x X0 X1)
        (one_below_x X1 X2)
        (one_below_x X2 X3)
        (one_below_x X3 X4)
        (below_x X0 X4) (below_x X0 X3) (below_x X0 X2) (below_x X0 X1)
        (below_x X1 X4) (below_x X1 X3) (below_x X1 X2)
        (below_x X2 X4) (below_x X2 X3)
        (below_x X3 X4)
        (one_above_x X1 X0)
        (one_above_x X2 X1)
        (one_above_x X3 X2)
        (one_above_x X4 X3)
        (above_x X4 X0) (above_x X4 X1) (above_x X4 X2) (above_x X4 X3)
        (above_x X3 X0) (above_x X3 X1) (above_x X3 X2)
        (above_x X2 X0) (above_x X2 X1)
        (above_x X1 X0)
        


        ; Description of the how are distributed the Y coordinates in the board
        (one_below_y Y0 Y1)
        (one_below_y Y1 Y2)
        (one_below_y Y2 Y3)
        (one_below_y Y3 Y4)
        (below_y Y0 Y4) (below_y Y0 Y3) (below_y Y0 Y2) (below_y Y0 Y1)
        (below_y Y1 Y4) (below_y Y1 Y3) (below_y Y1 Y2)
        (below_y Y2 Y4) (below_y Y2 Y3)
        (below_y Y3 Y4)
        (one_above_y Y1 Y0)
        (one_above_y Y2 Y1)
        (one_above_y Y3 Y2)
        (one_above_y Y4 Y3)
        (above_y Y4 Y0) (above_y Y4 Y1) (above_y Y4 Y2) (above_y Y4 Y3)
        (above_y Y3 Y0) (above_y Y3 Y1) (above_y Y3 Y2)
        (above_y Y2 Y0) (above_y Y2 Y1)
        (above_y Y1 Y0)
        


        ; Board coordinates of the robot in the initial position
        (robot_at_coordinatex robot1 X0)
        (robot_at_coordinatey robot1 Y0)


        ; Board coordinates of the ghost in the initial position
        (ghost_at_coordinatex ghost1 X3)
        (ghost_at_coordinatey ghost1 Y3)


        ; Ghost predefined positions across time
        (position_ghost X3 Y2 T1)
        (position_ghost X2 Y2 T2)
        ; (position_ghost X2 Y1 T3)
        ; (position_ghost X2 Y1 T4)
        ; (position_ghost X2 Y1 T5)
        ; (position_ghost X2 Y1 T6)


        ; Global variables
        (robot_movement true)
        (present_time   T0)
        (used_time T0)
    )

    (:goal
    ;this specifies that the goal of the plan is to be at the same place (robot and ghost)
        (and
            (in_the_same_place true)
        )
    )

    (
        ; take into consideration minimizing the cost when deciding the plan
        :metric minimize (total-cost)
    )

)
