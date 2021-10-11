(define (domain wumpus1)
    (:requirements :strips :negative-preconditions :typing) 
    (:types
        room
        who
    )

    (:predicates
    (adj ?rom-1 ?rom-2)
    (pit ?room)
    (havearow ?who)
    (havegold ?who)
    (dead ?who)
    (wump ?room)
    (agnt ?rom)
    (gld ?rom)
    )

    (:action move
        :parameters (?from - room ?to - room)
        :precondition   (and (adj ?from ?to)
                        (agnt ?from)
                        (not (wump ?to))
                        (not (pit ?to))
                        )

        :effect (and (not (agnt ?from))
                    (agnt ?to)
        )
    )

    (:action take
        :parameters (?who - who ?where - room)
        :precondition (and  (gld ?where)
                            (not (havegold ?who))
                            (agnt ?where)
                      )
        :effect (and (havegold ?who )
            (not (gld ?where)))
    )

    (:action shoot
        :parameters (?who - who ?from - room ?to - room )
        :precondition (and  (havearow ?who)
                            (wump ?to)
                            (agnt ?from)
                            (adj ?to ?from)
        )
                    
        :effect (and (not (wump ?to)) (not (havearow ?who)))
        
        )
    
)