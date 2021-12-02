# LECTURE 2: AGENT ARCHITECTURES

## Definitions of agent

1. An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through effectors.

2. Autonomous agents are computational systems that inhabit some complex dynamic environment, sense and act autonomously in this environment, and by doing so realize a set of goals or tasks for which they are designed

   

![](img/arquitectura_agent.JPG)

## Kinds of environments

* **Accessible**: agent can obtain complete, accurate, up-to-date information about the environment state.
* **Deterministic environment** : any action has a single guaranteed effect. The physical world can to all intents purposes be regarded as a non-deterministic. **Non-deterministic** environments present greater problems for the agent designer. 
* **Episodic**: The performance of an agent is dependent on a number of discrete, independent episodes, with no link between the performance of an agent in differrent scenarios. 
* **Static environment** : Static environment is one that can be assumed to remain unchanged except by the performance of actions by the agent
* **Dynamic environment**: A dynamic environment is one that has other processes operating on it, and which hence changes in ways beyond the agent’s control. The physical world and the Web are highly dynamic environments. It is hard to design and implement agents in dynamic environments
* **Discrete environment** Is discrete if there is a fixed, finite number of actions and percepts in it. Real world is a continuous environment. 

## Agent architectures

Two aspects define how the sensor data and the current internal state of the agent determine the actions (effector outputs) and the future internal state of the agent

![](img/architecture_agent.JPG)

### Types of agent architectures

1. **Reactive:** Focused on fast reactions/responses to changes detected in the environment.
2. **Deliberative**: Focused on a long-term planning of actions, centred on a set of basic goals.
3. **Hybrid:** Combining a reactive side and a deliberative side.



## Reactive agents 

Intelligence is a product of the interaction between an agent and its environment

### Main characteristics

* Simple agents
* Simple interaction
* Complex behaviour patterns appear as a result of the dynamic interactions
* The global behaviour of the system is not specified a prior
* Agents composed of autonomous modules
* Each module manages a given task
  * Sensor, control, computations
* Basic data from sensors

### Basic schema of reactive architecture

Reactive behaviour: action rules: **S** &#8594; **A ** where S denotes the states of the environment, and A the primitive actions the agent is capable of performing

![](img/schema_simple_agent.JPG)

### Subsumption hierarchy

* A subsumption architecture is a hierarchy of task-accomplishing behaviours.

* Each behaviour is a rather simple rule-like structure

* Each behaviour ‘competes’ with others to exercise control over the agent, as different behaviours may be applicable at the same time

#### Behaviour layers

* Lower layers represent primitive kinds of behaviour (such as avoiding obstacles) 
* Higher layers represent more complex behaviours (e.g. identifying an object) 
* Lower layers have precedence over layers further up the hierarchy 
* The resulting systems are, in terms of the amount of computation they do, extremely simple

**Exemple** 

![](img/exemple_behaviourlayers.JPG)



### Advantages of Reactive Agents

* Simplicity of individual agents 
* Flexibility, adaptability 
* Ideal in very dynamic and unpredictable environments
* Low computational cost 
* Robustness against failure
* Elegance

### Limitations of Reactive Agents

* Difficult to make reactive agents that learn dynamic evolution of rules



## Deliberative architecture 

* To do

## Hybrid Architectures

![](img/hybrid_architecture.JPG)

### Layering techniques

1. Horizontal layering

   * *m* psibble actions suggested by each layer, *n* layers

   ![](img/horitzontal_layering.JPG)

2. Vertical layering

   * *m* possible actions suggested by each layer, *n* layers

   ![](img/vertical_layering.JPG)

## Touring machines architecture

Consists of perception and action subsystems, which interface directly with the agent’s environment, and three control layers, embedded in a control framework, which mediates between the layers.

![](img/turing_machine.JPG)

* **Reactive layer** :  implemented as a set of situation-action rules (subsumption architecture)

* **Planning layer** : constructs plans and selects actions to execute in order to achieve the agent’s goals
* **Modeling layer** : contains symbolic representations of the ‘cognitive state’ of other entities in the agent’s environment

## InterRRaP ...

to do