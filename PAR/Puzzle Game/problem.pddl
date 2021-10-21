(define (problem PuzzleGame) (:domain p1)
(:objects 
    X0 X1 X2 X3 - board_coordinate_x
    Y0 Y1 Y2 Y3 - board_coordinate_y
    one two three four five six seven eight nine ten eleven twuelve thirteen fourthten fiveteen - value
)

(:init
        (below_x X0 X1)
        (below_x X1 X2)
        (below_x X2 X3)
        (above_x X1 X0)
        (above_x X2 X1)
        (above_x X3 X2)
        (below_y Y0 Y1)
        (below_y Y1 Y2)
        (below_y Y2 Y3)
        (above_y Y1 Y0)
        (above_y Y2 Y1)
        (above_y Y3 Y2)
        (atCell X0 Y0 one)
        (atCell X1 Y0 two)
        (atCell X2 Y0 three)
        (atCell X3 Y0 four)
        (atCell X0 Y1 five)
        (atCell X1 Y1 six)
        (atCell X2 Y1 seven)
        (atCell X3 Y1 eight)
        (atCell X0 Y2 nine)
        (atCell X1 Y2 ten)
        (atCell X2 Y2 eleven)
        (atCell X3 Y2 twuelve)
        (atCell X0 Y3 thirteen)
        (atCell X1 Y3 fourthten)
        (atCell X3 Y3 fiveteen)
        (whereWhite X2 Y3)
        
)

    ;todo: put the initial state's facts and numeric values here


(:goal (and
        (atCell X0 Y0 one)
        (atCell X1 Y0 two)
        (atCell X2 Y0 three)
        (atCell X3 Y0 four)
        (atCell X0 Y1 five)
        (atCell X1 Y1 six)
        (atCell X2 Y1 seven)
        (atCell X3 Y1 eight)
        (atCell X0 Y2 nine)
        (atCell X1 Y2 ten)
        (atCell X2 Y2 eleven)
        (atCell X3 Y2 twuelve)
        (atCell X0 Y3 thirteen)
        (atCell X1 Y3 fourthten)
        (atCell X2 Y3 fiveteen)
        (whereWhite X3 Y3)
    ;todo: put the goal condition here
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
