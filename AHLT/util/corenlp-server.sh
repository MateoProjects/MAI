#!/usr/bin/env bash
#
# Runs Stanford CoreNLP server

# set this path to the directory where you decompressed StanfordCore
STANFORD_CONTAINER_DIR=~/Software
mkdir -p $STANFORD_CONTAINER_DIR
STANFORDDIR=$STANFORD_CONTAINER_DIR/stanford-corenlp-4.4.0

# Download dependencies (java (default-jre) and standford-corenlp.4.4.0)
if java -version 2&> /dev/null; then
  echo "Java already installed"
else
  echo "Installing Java"
  sudo apt-get install default-jre
  if [ $? -eq 0 ]; then
    echo "Java correctly installed"
  else
    echo "ERROR while installing Java"
    exit 1
  fi
fi
if [ -d $STANFORDDIR ]; then
  echo "Standford Core NLP already installed"
else
  echo "Installing Standford Core NLP"
  wget https://nlp.stanford.edu/software/stanford-corenlp-latest.zip && \
  unzip stanford-corenlp-latest.zip -d $STANFORD_CONTAINER_DIR && \
  rm stanford-corenlp-latest.zip

  if [ $? -eq 0 ]; then
    echo "Standford Core NLP correctly installed"
  else
    echo "ERROR while installing Standford Core NLP"
    exit 2
  fi
fi

if [ -f /tmp/corenlp-server.running ]; then
    echo "server already running"
else
    echo java -mx5g -cp \"$STANFORDDIR/*\" edu.stanford.nlp.pipeline.StanfordCoreNLPServer $*
    java -mx5g -cp "$STANFORDDIR/*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer $* &
    echo $! > /tmp/corenlp-server.running
    wait
    rm /tmp/corenlp-server.running
  fi
