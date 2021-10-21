(define (problem PuzzleGame) (:domain p1)
(:objects 
    X0 - board_coordinate_x X1 - board_coordinate_x
    X2 - board_coordinate_x X3 - board_coordinate_x
    Y0 - board_coordinate_y Y1 - board_coordinate_y
    Y2 - board_coordinate_y Y3 - board_coordinate_y
    one - value
    two - value  
    three - value
    four - value
    five - value 
    six - value
    seven - value
    eight - value
    nine - value
    ten - value
    eleven - value
    twelve - value
    thirteen - value
    fourteen - value
    fiveteen - value
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
        (atCell X0 Y0 fiveteen)
        (atCell X1 Y0 ten)
       ; (atCell X2 Y0 three)
        (atCell X3 Y0 thirteen)
        (atCell X0 Y1 eleven)
        (atCell X1 Y1 four)
        (atCell X2 Y1 one)
        (atCell X3 Y1 twelve)
        (atCell X0 Y2 three)
        (atCell X1 Y2 seven)
        (atCell X2 Y2 nine)
        (atCell X3 Y2 eight)
        (atCell X0 Y3 two)
        (atCell X2 Y3 six)
        (atCell X1 Y3 fourteen)
        (atCell X3 Y3 five)
        (whiteIn X2 Y0)        
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
        (atCell X3 Y2 twelve)
        (atCell X0 Y3 thirteen)
        (atCell X1 Y3 fourteen)
        (atCell X2 Y3 fiveteen)
        (whiteIn X3 Y3)
    ;todo: put the goal condition here
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
