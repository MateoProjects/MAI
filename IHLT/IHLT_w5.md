# Semantics

Semantics deals with the meaning:

* Lexical semantics: deals with the meaning of individual words
* Compositional semantics

The motivation of lexical semantics is discover pattern, relations etc...

Knowledge-based resources: represented as graphs. For example **WordNet**

Corpus-based resources: contextual usage of words.



## WordNet

* Free large lexical database of English

  Contains only nouns, verbs, adjectives and adverbs

* Words are grouped into synonyms sets (synsets)

* each synset has an associated gloss and some examples

* synsets are interlinked by means of lexical relations

**Example of lexical relation net**

*need to add photo*

Ones of the most important lexical relations are:

* Synonym
* Hypernym
* Hyponym



### Similarities in WordNet

* Shortest Path Length: 
  $$
  Sim(s_1, s_2) = 1 / (1+SPL(s_1, s2_2))
  $$

* Leacock & Chodorow:
  $$
  Sim(s_1, s2_) = -log · (1+SPL(s_1,s_2)) / 2·MaxDepth
  $$
  
* Wu & Palmer:

$$
Sim(s_1, s_2) = 2·depth(LCS(s_1,s_2)) / depth_{LCS(s_1,s_2)}(s_1) + depth_{LCS(s_1,s_2)}(s_2)
$$

* Lin

$$
Sim(s_1,s_2) = 2·IC(LCS(s_1, S_2)) / IC(s_1) + IC(s_2)
$$

---

## SentiWordNet

Extension of wordnet that adds for each synset 3 measures:

* positive score
* negative score
* objective score = 1 - positive_score - negative_score

to_do: *Add table example*

## Sentiment analysis

Different subtasks:

* **Opinion detection**: given a piece of text (document etc..), is it an objective text or subjective one?
* **Polarity classification**: given a subjective piece of text, is it a positive opinion or negative one?
* **Opinion extraction**: given a subjective piece of text recognize the focuses of the opinion



Unsupervised sentiment analysis

* Possible solution:
  $$
  h(D) = \sum_{s\in D} score(s)
  $$
   

  D is usually the set of synsets related to adjectives, or to nouns and adjectives, or to nouns, verbs, adjectives and adverbs.

* Opinion detection:
  $$
  score(s) = 1 - obj_s \ \ or \ \ score(s) =obj_s
  $$

* ..-



Supervised sentiment analysis

* Possible solution:

  Bag of words with Naïve Bayes
  $$
  h(D) = h(w_1,...,w_n) = argmaxP(y)\prod_{i=1}^n P(w_i|y)
  $$
  where *y* is the category(positive/negative, subjective/objective), and w1,...,wn is the bag of words related to *D*

  * Given a training corupus *C={di}* partitioned into subsets Y1 and Y2

    * $$
      P(y)\sim P_MLE(y) = ...
      $$

    * 

* Pros:
  * Higher results
  * no need for POS and WSD taggers
* Cons
  * need for training corpora
