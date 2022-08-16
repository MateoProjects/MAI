## ------------------- 
## -- check pattern:  LCS is a verb, one entity is under its "nsubj" and the other under its "obj"
def check_LCS_svo(tree,tkE1,tkE2):
   if tkE1 is not None and tkE2 is not None:
      lcs = tree.get_LCS(tkE1,tkE2)
      
      #  If it's verb and not negated
      if tree.get_tag(lcs)[0:2] == "VB" and tree.get_word(lcs-1) != "not":
         path1 = tree.get_up_path(tkE1,lcs)
         path2 = tree.get_up_path(tkE2,lcs)
         func1 = tree.get_rel(path1[-1]) if path1 else None
         func2 = tree.get_rel(path2[-1]) if path2 else None
         
         if (func1=='nsubj' and func2=='obj') or (func1=='obj' and func2=='nsubj'):
            lemma = tree.get_lemma(lcs).lower()
            if lemma in ['diminish','augment','exhibit','experience','counteract',
            'potentiate','enhance','reduce','antagonize']: # reduce, antagonize are ambiguous
               return 'effect'
            if lemma in ['impair','inhibit','displace','accelerate','bind','induce',
            'decrease','elevate','delay']:   # DECREASE, inhibit, displace, induce, elevate, delay are ambiguous
               return 'mechanism'
            if lemma in ['exceed']:
               return 'advise'
            if lemma in ['suggest']:   # SUGGEST is ambiguous
               return 'int'
         
   return None


## ------------------- 
## -- check pattern:  A word in between both entities belongs to certain list
def check_wib(tree,tkE1,tkE2,entities,e1,e2):
   if tkE1 is not None and tkE2 is not None:
      # get actual start/end of both entities
      l1,r1 = entities[e1]['start'],entities[e1]['end']
      l2,r2 = entities[e2]['start'],entities[e2]['end']
      
      for t in range(tkE1+1,tkE2):
         # get token span
         l,r = tree.get_offset_span(t)
         # if the token is in between both entities and it's not negated
         if r1 < l and r < l2 and tree.get_word(t-1) != "not":
            lemma = tree.get_lemma(t).lower()
            if lemma in ['tendency','stimulate','regulate','prostate','modification',
            'augment','accentuate','exacerbate','proliferation','rarely','secondary']: # proliferation, rarely, secondary added
               return 'effect'
            if lemma in ['react','faster','presumably','induction','substantially',
            'minimally','delay','induce','modest','induction']: # delay, induce, modest, induction added | DELAY, INDUCE, substantially, minimally are ambiguous
               return 'mechanism'
            if lemma in ['exceed','extreme','cautiously','should']: # should added | SHOULD is ambiguous
               return 'advise'
            if lemma in ['interact']:  # interact is ambiguous
               return 'int'
            
            # if tree.is_entity(tk, entities)

   return None

## ------------------- 
## -- check_LCS_VB_NN:  If the LCS is a verb or a noun (not negated), check it
## -- Designed to exploit the misses of "check_LCS_svo" (when func(1|2)!='nsubj' and func(1|2)!='obj')
def check_LCS_VB_NN(tree, tkE1, tkE2):
   if tkE1 is not None and tkE2 is not None:
      lcs = tree.get_LCS(tkE1,tkE2)
      
      # If it's verb or a noun and not negated
      if tree.get_tag(lcs)[0:2] in ["VB","NN"] and tree.get_word(lcs-1) != "not":
         lemma = tree.get_lemma(lcs).lower()
         if lemma in ['accentuate', 'counteract', 'augment', 'combine', 'diminish',
          'regulate', 'enhance', 'injection', 'potentiate']: # injection, potentiate are ambiguous
            return 'effect'
         if lemma in ['impair', 'accelerate', 'react']:  # accelerate and react may be ambiguous
            return 'mechanism'
         if lemma in ['exceed', 'titrate', 'avoid', 'prescribe']:
            return 'advise'
   
   return None

## ------------------- 
## -- check_LCS_VB_rels:  If the LCS is a verb (not negated), check the relations of entities with it.
#  -- Designed to solve ambiguities
def check_LCS_VB_rels(tree, tkE1, tkE2):
   if tkE1 is not None and tkE2 is not None:
      lcs = tree.get_LCS(tkE1,tkE2)

      # If it's verb or a noun and not negated
      if tree.get_tag(lcs)[0:2] == "VB" and tree.get_word(lcs-1) != "not":
         path1 = tree.get_up_path(tkE1,lcs)
         path2 = tree.get_up_path(tkE2,lcs)
         func1 = tree.get_rel(path1[-1]) if path1 else None
         func2 = tree.get_rel(path2[-1]) if path2 else None

         # If both functions are different from None
         if func1 is not None and func2 is not None:
            lemma = tree.get_lemma(lcs).lower()
            lemma_f1_f2 = f"{lemma}_{func1}_{func2}"
            lemma_f1 = f"{lemma}_{func1}"

            # Some particular cases
            if lemma_f1_f2 in ['potentiate_nsubj:pass_obl', 'accentuate_nsubj:pass_obl']:
               return 'effect'
            if lemma_f1 in ['antagonize_nsubj:pass']:
               return 'effect'
            if lemma_f1_f2 in ['impair_nsubj:pass_obl', 'increase_nsubj:pass_obl']:
               return 'mechanism'
            if lemma_f1_f2 in ['interact_nsubj_obl']:
               return 'int'
   
   return None


def check_LCS_VB_parent(tree,tkE1,tkE2):
   if tkE1 is not None and tkE2 is not None:
      lcs = tree.get_LCS(tkE1, tkE2)
      if tree.get_tag(lcs)[0:2] == "VB":
         parent = tree.get_parent(lcs)
         if parent is not None and tree.get_tag(parent)[0:2] == "VB":
            parent_and_lcs = tree.get_lemma(parent).lower() + "_" + tree.get_lemma(lcs).lower()
            if parent_and_lcs in ['show_inhibit']:
               return 'mechanism'
            if parent_and_lcs in ['occur_administer', 'report_diminish', 'suggest_regulate']:
               return 'effect'
            if parent_and_lcs in ['recommend_use']:
               return 'advise'
            if parent_and_lcs in ['affect_interact']:
               return 'int'

   return None