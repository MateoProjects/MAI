
			 SEMEVAL-2012 TASK 17

				 STS
		     Semantic Textual Similarity:
 
		     A Unified Framework for the
	      Evaluation of Modular Semantic Components



The trial dataset contains the following:

  00-README.txt		  this file
  STS.input.txt		  tab separated input file with ids and sentence pairs
  STS.gs.txt	  	  tab separated gold standard
  STS.output.txt	  tab separated sample output



Introduction
------------

Given two sentences of text, s1 and s2, the systems participating in
this task should compute how similar s1 and s2 are, returning a
similarity score, and an optional confidence score.

The dataset comprises pairs of sentences drawn from publicly
available datasets:

- MSR-Paraphrase, Microsoft Research Paraphrase Corpus
  http://research.microsoft.com/en-us/downloads/607d14d9-20cd-47e3-85bc-a2f65cd28042/

- MSR-Video, Microsoft Research Video Description Corpus
  http://research.microsoft.com/en-us/downloads/38cf15fd-b8df-477e-a4e4-a4680caa75af/

The train data will also include pairs of sentences drawn from machine
translation evaluation exercises, after clearing license issues.

The sentence pairs have been manually tagged with a number from 0 to
5, as defined below (cf. Gold Standard section). 

NOTE: Participant systems should not use the test part of
MSR-Paraphrase to develop or train their system.



License
-------

All participants need to agree with the license terms from Microsoft Research:

http://research.microsoft.com/en-us/downloads/607d14d9-20cd-47e3-85bc-a2f65cd28042/
http://research.microsoft.com/en-us/downloads/38cf15fd-b8df-477e-a4e4-a4680caa75af/




Input format
------------

The input file consist of three fields separated by tabs:

- unique id of pair
- first sentence (does not contain tabs)
- second sentence (does not contain tabs)

Please check STS.input.txt



Gold Standard
-------------

The gold standard contains a score between 0 and 5 for each pair of
sentences, with the following interpretation:

(5) The two sentences are completely equivalent, as they mean the same
    thing.  

      The bird is bathing in the sink.  
      Birdie is washing itself in the water basin.

(4) The two sentences are mostly equivalent, but some unimportant
    details differ.

      In May 2010, the troops attempted to invade Kabul.
      The US army invaded Kabul on May 7th last year, 2010.

(3) The two sentences are roughly equivalent, but some important
    information differs/missing.

      John said he is considered a witness but not a suspect.
      "He is not a suspect anymore." John said.

(2) The two sentences are not equivalent, but share some details.

      They flew out of the nest in groups.
      They flew into the nest together.

(1) The two sentences are not equivalent, but are on the same topic.

      The woman is playing the violin.
      The young lady enjoys listening to the guitar.

(0) The two sentences are on different topics.

      John went horse back riding at dawn with a whole group of friends.
      Sunrise at dawn is a magnificent view to take in if you wake up
      early enough for it.

Format: the gold standard file consist of two fields separated by tabs:

- unique id of pair
- a number between 0 and 5

Please check STS.gs.txt



Answer format
--------------

The answer format is similar to the gold standard format, but includes
an optional confidence score. 

- unique id of pair
- a number between 0 and 5 (the similarity score)
- a number between 0 and 100 (the confidence score)

Please check STS.output.txt



Scoring
-------

The scoring will be based on Pearson correlation. The script will be
released with the training data.



Other
-----

Please check http://www.cs.york.ac.uk/semeval/task17/ for more details.

We recommend that potential participants join the task mailing list:

 http://groups.google.com/group/STS-semeval



