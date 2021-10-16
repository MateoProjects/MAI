# Wumpus game

## Introduction and explanation of two solutions
<br>

The differences between both solutions are in actions that agent can do it. In the second solution we specify all actions that agent can do meanwhile, in first solution there are only three general actions but it's restricted by other conditions that need to complish before realize the action. 



### **Solution 1**


* In this solution we represent the game with rooms. We will check if in room are wumpus or agent and can move to other room.  If in room is in agent then it will check if it's possible move agent to other room, can shoot the wumpus or take gold.
<br>

* In this solution there are only three actions . move , take or shoot. 
* 

**Actions and definitions**


* Move
  * **Parameters**: from , to
  * **Preconditions**: agent need to stay in room "from" and room "to" need to bé on next to. for enable move. 
  * **Effect**: Agent move room "from" to room "to"

* take
  * **Parameters**: who , where
  * **Preconditions**: gold need to stay on room "where" and agent not have gold at this moment. Last precondition is agent need to stay on room "where" 
  * **Effect**: Agent take gold from room "where"


* shoot
  * **Parameters**: who, from to
  * **Preconditions**: Agent need to have arrow, wumpus need to be on room "to" and agent need to be on room "from". Finally the last condition is that rooms "to" and "from" need to be adjacent
  * **Effect**: wumpus die.



---

### **Solution 2**

* In this solution the posible actions that can do agent is diferent. In this solution the actions will be represent the actions that agent can do it. 
* The possible actions that agent can do are Move-left, move-right , move-up, move-down, take (gold if it's possible), shot (if it's possible).  

**Actions and definitions**

<br>

* move-left
  * **Parameters**: f1, f2, c1 c2 agent, wumpus, pit
  * **Preconditions**: pit and wumpus are not on f2-c2, c1 is greater column than c2, agent is in f1 c1 and finally f1-c1 and f2-c2 are adjunts squares
  * **Effect**: Agent move to f2-c2 from f1-c1

* move-right
  * **Parameters**: f1, f2, c1 c2 agent, wumpus, pit
  * **Preconditions**: pit and wumpus are not on f2-c2, c2 is greater column than c1, agent is in f1 c1 and finally f1-c1 and f2-c2 are adjunts squares
  * **Effect**: Agent move to f2-c2 from f1-c1
  
* move-up
  * **Parameters**: f1, f2, c1 c2 agent, wumpus, pit
  * **Preconditions**:  pit and wumpus are not on f2-c2, f1 is greater row than f2, agent is in f1 c1 and finally f1-c1 and f2-c2 are adjunts squares
  * **Effect**: Agent move to f2-c2 from f1-c1
  
* move-down
  * **Parameters**: f1, f2, c1 c2 agent, wumpus, pit
  * **Preconditions**: pit and wumpus are not on f2-c2, f2 is greater row than f1, agent is in f1 c1 and finally f1-c1 and f2-c2 are adjunts squares
  * **Effect**: Agent move to f2-c2 from f1-c1


* shot
  * **Parameters**: f1, f2, c1 c2 agent, wumpus
  * **Preconditions**: agent need to have arrow and is in f1-c1, wumpus is live and is in f2-c2. Finally f1-c1 and f2-c2 need to be adjunct squares
  * **Effect**: wumpus die. Now there are nothing on f2-c2 and agent haven't arrow.

* take
  * **Parameters**: f1, c1, agent, gold
  * **Preconditions**: object gold is in f1-c1 and agent is in f1-c1
  * **Effect**: agent take gold. Gold now is not in f1-c1
 