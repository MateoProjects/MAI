# Sequence Prediction

* HMM:
  * Recordar que HMM eran grafs, i es calcula la prob d'anar de un node a un altre. 
* Refrescar el viterbi algorithm de IHLT

Ex1 Features AHLT 

* Vocabulary = 100
* word history x = (x1..., xi-1)
* size of alphabet is 26
* 4-letter suffix

​	1 if y = u and xi_1 ends with s

How many possible features are there in this model?

* Potential space is 1000 x 26^4

Ex2 Training size n = 10k . Which is a good upper bound on the number of features introduced by this training set

* Solution : 10.000 perque generarà dif paraules. 

Ex10 

We are performing PoS tagging for a recently discovered alien language using a trigam factored crf, using tagset T = {D,V,N,A,P} and we defined a history as h = ...

How many possible histories are there for a given input squence X and a fixed value of i? Justify your answer

* 25

2. 

3. 