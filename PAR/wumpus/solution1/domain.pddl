;Header and description

(define (domain domain_name)

;remove requirements that are not needed
(:requirements :strips :typing :conditional-effects  :equality :negative-preconditions)

(:types 
    wumpus - object
    agent - object
    gold - object
)

; un-comment following line if constants are needed
;(:constants )

(:predicates 
(on ?square)
(adj ?square1 ?square2)  ; 
(gold_on ?square ) ; is gold on square
(at ?elem ?square) ; what are in square
(dead ?elem) ; for check ifagent is dead
(take ?what)
(have ?who ?what)
(wumpus ?square)
(arrow ?what)
)

(:action take ; take gold
    :parameters (?who ?what ?square)
    :precondition   (and (dead ?who)
                    (take ?what) 
                    (at ?who ?square)
                    (at ?what ?square)
                    )
    :effect (and (have ?who ?what) 
                (not (at ?what ?square)))
    
)



(:action move
    :parameters (?who ?square ?squareto )
    :precondition (and  (not (dead ?who))
                        (adj ?square ?squareto)
                        (not (wumpus ?squareto))

                )
    :effect (and (not (at ?who ?square))
                (at ?who ?squareto)) 
)


(:action shot ; shot wumpus
    :parameters (?agent ?arrow ?square ?squarew  ?wumpus) 
    :precondition   (and (not (dead ?agent))
                        (adj ?square ?squarew)
                        (arrow ?arrow)
                        (not (dead ?wumpus))
                        (have ?agent ?arrow)
                        (at ?agent ?square)
                        (at ?wumpus ?squarew)
                    )
    :effect (and    (dead ?wumpus)
                    (not(at ?wumpus ?square))
                    (not(have ?agent ?arrow))
            )
)
)





