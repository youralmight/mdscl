#!/usr/bin/env bash
set -e

read -r -p "Your name: " name
read -r -p "Where are you from? " hometown
read -r -p "What did you study or do before MDS? " background
read -r -p "What do you hope to get from MDS? " goal

set -x
mkdir DSCI_521-milestone_1
cd DSCI_521-milestone_1
mkdir data documents screenshots
cat > README.md <<EOF
# DSCI 521 Milestone 1

## About me

My name is ${name}. I am from ${hometown}. Before MDS, I studied or worked in ${background}. Through the MDS program, I hope to ${goal}.

## About this milestone

This milestone contains my README and the data, documents, and screenshots folders. It records my practice with Bash commands and file organization.
EOF
ls
ls data
ls documents
set +x

printf '\nDone. Now run: history\n'
printf 'Then take screenshots of this terminal, the history output, and README.md.\n'
