;Header and description

(define (domain wumpus2)

;remove requirements that are not needed
(:requirements :strips :fluents :adl :typing :conditional-effects :negative-preconditions )

(:types ;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
    wumpus - object
    agent - object
    gold - object
    pit - object
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
    (gtcol ?c1 ?c2 ) ; checks if x1 > x2
    (gtrow ?f1  ?f2 ) ; checks if row x1 > x2
    (havearow ?who)
    (what ?f1 ?c2 ?who)
    (die ?who)
    (haveGold ?who)

)



(:action move-left
    :parameters (?f1 ?f2 ?c1 ?c2 ?agent ?wumpus ?pit)
    :precondition (and  
                        (not (what ?f2 ?c2 ?pit))
                        (gtcol ?c1 ?c2)
                        (what ?f1 ?c1 ?agent)
                        (not (what ?f2 ?c2 ?wumpus))

    )
    :effect (and (not (what ?f1 ?c1 ?agent)) (what ?f2 ?c2 ?agent))
)

(:action move-right
   :parameters (?f1 ?f2 ?c1 ?c2 ?agent ?wumpus ?pit)
    :precondition (and 
                        (not (what ?f2 ?c2 ?pit))
                        (gtcol ?c2 ?c1)
                        (what ?f1 ?c1 ?agent)
                        (not (what ?f2 ?c2 ?wumpus))

    )
    :effect (and (not (what ?f1 ?c1 ?agent)) (what ?f2 ?c2 ?agent))
)

(:action move-up
    :parameters (?f1 ?f2 ?c1 ?c2 ?agent ?wumpus ?pit)
    :precondition (and  
                        (not (what ?f2 ?c2 ?pit))
                        (gtrow ?f1 ?f2)
                        (what ?f1 ?c1 ?agent)
                        (not (what ?f2 ?c2 ?wumpus))

    )
    :effect (and (not (what ?f1 ?c1 ?agent)) (what ?f2 ?c2 ?agent))
)

(:action move-down
    :parameters (?f1 ?f2 ?c1 ?c2 ?agent ?wumpus ?pit)
    :precondition (and  
                        (not (what ?f2 ?c2 ?pit))
                        (gtrow ?f2 ?f1)
                        (what ?f1 ?c1 ?agent)
                        (not (what ?f2 ?c2 ?wumpus))

    )
    :effect (and (not (what ?f1 ?c1 ?agent)) (what ?f2 ?c2 ?agent))
)

(:action shot
    :parameters (?f1 ?f2 ?c1 ?c2 ?agent ?wumpus)
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
    :parameters (?f1 ?c1 ?agent ?gold)
    :precondition (and  (what ?f1 ?c1 ?gold)
                        (what ?f1 ?c1 ?agent)
    )
    :effect (and    (haveGold ?agent)
                    (not (what ?f1 ?c1 ?gold))
    )
)




;define actions here

)