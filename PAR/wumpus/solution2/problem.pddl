(define (problem wumpus_game) (:domain wumpus2)
(:objects 
    c1 - columna c2 - columna c3 - columna f1 - fila f2 - fila pit - pit wumpus - wumpus agent - agent gold - gold
)
;   g p x
;   w x a
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
    (squareadj f1 c1 f1 c2) (squareadj f1 c2 f1 c1)
    (squareadj f1 c2 f1 c3) (squareadj f1 c3 f1 c2)
    (squareadj f2 c1 f2 c2) (squareadj f2 c2 f2 c1)
    (squareadj f2 c2 f2 c3) (squareadj f2 c3 f2 c2)
    (squareadj f1 c1 f2 c1) (squareadj f2 c1 f1 c1)
    (squareadj f1 c2 f2 c2) (squareadj f2 c2 f1 c2)
    (squareadj f1 c3 f2 c3) (squareadj f2 c3 f1 c3)
    )

(:goal (and  (haveGold agent)(what f2 c3 agent))))
