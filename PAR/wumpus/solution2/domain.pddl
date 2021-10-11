;Header and description

(define (domain wumpus2)

;remove requirements that are not needed
(:requirements :strips :fluents :adl :typing :conditional-effects :negative-preconditions )

(:types
    fila 
    columna
    agent 
    wumpus 
    pit
    gold
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    (gtcol ?c1 ?c2 ) ; checks if x1 > x2
    (gtrow ?f1  ?f2 ) ; checks if row x1 > x2
    (havearow ?who)
    (what ?f1 ?c1 ?who)
    (die ?who)
    (haveGold ?who)

)



(:action move-left
    :parameters (?f1 - fila ?f2 - fila ?c1 - columna ?c2 - columna ?agent - agent ?wumpus - wumpus ?pit - pit)
    :precondition (and  
                        (not (what ?f2 ?c2 ?pit))
                        (gtcol ?c1 ?c2)
                        (what ?f1 ?c1 ?agent)
                        (not (what ?f2 ?c2 ?wumpus))

    )
    :effect (and (not (what ?f1 ?c1 ?agent)) (what ?f2 ?c2 ?agent))
)

(:action move-right
   :parameters (?f1 - fila ?f2 - fila ?c1 - columna ?c2 - columna ?agent - agent ?wumpus - wumpus ?pit - pit)
    :precondition (and 
                        (not (what ?f2 ?c2 ?pit))
                        (gtcol ?c2 ?c1)
                        (what ?f1 ?c1 ?agent)
                        (not (what ?f2 ?c2 ?wumpus)))

    
    :effect (and (not (what ?f1 ?c1 ?agent)) (what ?f2 ?c2 ?agent))
)

(:action move-up
    :parameters (?f1 - fila ?f2 - fila ?c1 - columna ?c2 - columna ?agent - agent ?wumpus - wumpus ?pit - pit)
    :precondition (and  
                        (not (what ?f2 ?c2 ?pit))
                        (gtrow ?f1 ?f2)
                        (what ?f1 ?c1 ?agent)
                        (not (what ?f2 ?c2 ?wumpus))

    )
    :effect (and (not (what ?f1 ?c1 ?agent)) (what ?f2 ?c2 ?agent))
)

(:action move-down
    :parameters (?f1 - fila ?f2 - fila ?c1 - columna ?c2 - columna ?agent - agent ?wumpus - wumpus ?pit - pit)
    :precondition (and  
                        (not (what ?f2 ?c2 ?pit))
                        (gtrow ?f2 ?f1)
                        (what ?f1 ?c1 ?agent)
                        (not (what ?f2 ?c2 ?wumpus))

    )
    :effect (and (not (what ?f1 ?c1 ?agent)) (what ?f2 ?c2 ?agent))
)

(:action shot
    :parameters (?f1 - fila ?f2 - fila ?c1 - columna ?c2 - columna ?agent - agent ?wumpus - wumpus)
    :precondition (and  (havearow ?agent)
                        (not (die ?wumpus))
                        (what ?f2 ?c2 ?wumpus)
                        (what ?f1 ?c1 ?agent)
    )
    :effect (and    (not(havearow ?agent))
                    (die ?wumpus)
                    (not (what ?f2 ?c2 ?wumpus))
    )
)

(:action take 
    :parameters (?f1 - fila ?c1 - columna ?agent - agent ?gold - gold)
    :precondition (and  (what ?f1 ?c1 ?gold)
                        (what ?f1 ?c1 ?agent)
    )
    :effect (and    (haveGold ?agent)
                    (not (what ?f1 ?c1 ?gold))
    )
)




;define actions here

)