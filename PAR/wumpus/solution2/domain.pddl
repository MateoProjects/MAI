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
    (gtcol ?x1 ?x2 ) ; checks if x1 > x2
    (gtrow ?x1  ?x2 ) ; checks if row x1 > x2
    (havearow ?who)
    (what ?x1 ?x2 ?who)
    (die ?who)
    (haveGold ?who)

)



(:action move-left
    :parameters (?x1 ?x2 ?y1 ?y2 ?agent ?wumpus ?pit)
    :precondition (and  (not(die ?agent))
                        (not (what ?x2 ?y2 ?pit))
                        (gtcol ?x1 ?x2)
                        (what ?x1 ?y1 ?agent)
                        (not (what ?x2 ?y2 ?wumpus))

    )
    :effect (and (not (what ?x1 ?x1 ?agent)) (what ?x2 ?y2 ?agent))
)

(:action move-right
   :parameters (?x1 ?x2 ?y1 ?y2 ?agent ?wumpus ?pit)
    :precondition (and  (not(die ?agent))
                        (not (what ?x2 ?y2 ?pit))
                        (gtcol ?x2 ?x1)
                        (what ?x1 ?y1 ?agent)
                        (not (what ?x2 ?y2 ?wumpus))

    )
    :effect (and (not (what ?x1 ?x1 ?agent)) (what ?x2 ?y2 ?agent))
)

(:action move-up
    :parameters (?x1 ?x2 ?y1 ?y2 ?agent ?wumpus ?pit)
    :precondition (and  (not(die ?agent))
                        (not (what ?x2 ?y2 ?pit))
                        (gtrow ?y2 ?y1)
                        (what ?x1 ?y1 ?agent)
                        (not (what ?x2 ?y2 ?wumpus))

    )
    :effect (and (not (what ?x1 ?x1 ?agent)) (what ?x2 ?y2 ?agent))
)

(:action move-down
    :parameters (?x1 ?x2 ?y1 ?y2 ?agent ?wumpus ?pit)
    :precondition (and  (not(die ?agent))
                        (not (what ?x2 ?y2 ?pit))
                        (gtrow ?y1 ?y2)
                        (what ?x1 ?y1 ?agent)
                        (not (what ?x2 ?y2 ?wumpus))

    )
    :effect (and (not (what ?x1 ?x1 ?agent)) (what ?x2 ?y2 ?agent))
)

(:action shot
    :parameters (?x1 ?x2 ?y1 ?y2 ?agent ?wumpus)
    :precondition (and  (havearow ?agent)
                        (not (die ?wumpus))
                        (what ?x2 ?y2 ?wumpus)
                        (what ?x1 ?y1 ?agent)
    )
    :effect (and    (not(havearow ?agent))
                    (die ?wumpus)
                    (not (what ?x2 ?y2 ?wumpus))
    )
)

(:action take
    :parameters (?x1 ?y1 ?agent ?gold)
    :precondition (and  (what ?x1 ?y1 ?gold)
                        (what ?x1 ?y1 ?agent)
                        (not (die ?agent))
    )
    :effect (and    (haveGold ?agent)
                    (not (what ?x1 ?y1 ?gold))
    )
)




;define actions here

)