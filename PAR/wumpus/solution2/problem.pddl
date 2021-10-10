(define (problem wumpus_game) (:domain wumpus2)
(:objects 
    c1 c2 c3 f1 f2 pit wumpus arrow agent gold
)

(:init
    (gtcol c2 c1)
    (gtcol c3 c2)
    (gtrow f2 f1)
    (havearow agent)
    (not (haveGold agent))
    (what f1 c2 pit)
    (what f1 c1 gold)
    (what f2 c1 wumpus)
    (what f2 c3 agent)
    ;todo: put the initial state's facts and numeric values here
)

(:goal (and (what f2 c3 agent) (haveGold agent)
    ;todo: put the goal condition here
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
