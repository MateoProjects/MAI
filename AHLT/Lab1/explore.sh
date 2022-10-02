#!/bin/bash
# This scripts gets the words of the $1 type from the training set

if (($# < 1))
then
  echo "The type (drug, drug_n, brand or group) is required as parameter"
  exit 1
fi

python3 ../util/ner2gold.py ../data/train | cut -d'|' -f3,4 | grep "|$1" | cut -d'|' -f1 | python3 -c "import sys; [print(x.strip()) for x in sys.stdin.readlines()]" | sort | uniq -c | sort -k1 -n
