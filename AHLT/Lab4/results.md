# Results
* Base (features in between + paths to LCS + path from E1 to E2): 47.2%

## Features not between the entities (+8.7% = 55.9%)
* Features previous to E1: 47.5% (+0.3%)
* Features previous to E2: 52.4% (+5.2%)
* Both: 54.9% (+7.7%)
    * \+ Removing redundant features (lemma and word removed, only lemma_tag): 55.9% (+8.7%) &larr; **NEW BEST**

## Adding more specific and general path features (+1.1% = 57.0%)
* Tag_Relation: 57.0% (+1.1%) &larr; **NEW BEST**
* Tag_Lemma: 54.9% (-1%)
* Tag_Relation & Tag_Lemma: 56.9% (+1%)

## Adding a information about LCS (+1.8% = 58.8%)
* Tag & Lemma: 58.8% (+1.8%) &larr; **NEW BEST**
  * \+ If VB, previous lemma: 57.9% (prev-0.9%)

## For other entity located previous, in between or after the corresponding entities (-1.3%, discarded)
* Check if shares LCS: 57.5% (-1.3%)

## Rule-based patterns from Lab3 (+0.7% = 59.5%)
* check_wib: 57.5% (-1.3%)
* check_wib less ambiguous: 58.5% (best-0.3% but prev+1%)
* check_LCS_svo: 58.6% (-0.2%)
* check_LCS_svo less ambiguous: 59.5% (best+0.7% and prev+1%) &larr; **NEW BEST**
* (check_LCS_svo + check_wib) less ambiguous: 58.5% (-0.3%)
* (check_LCS_svo + check_wib) less ambiguous and in cascade: 59.2% (-0.4%)
* (check_LCS_svo + check_LCS_VB_NN) less ambiguous and in cascade: 59.2% (-0.4%)
* (check_LCS_svo + check_LCS_VB_NN) less ambiguous: 59.1% (-0.5%)

## Don't consider stopwords at paths (-0.2%, discarded)
* For all paths: 59.3% (-0.2%)

## Consider ancestors and children
* Lemma & Tag from ancestors of E1 and E2: 59.2% (-0.3%)
* Lemma & Tag from children of ancestors (bros) of LCS: 60.3% (+0.8%)
  * \+ Discard features from tokens previous to E1: 59.0% (-1.3%)
  * \+ Add also ancestors: 60.7 (+1.2%)  &larr; **NEW BEST**
