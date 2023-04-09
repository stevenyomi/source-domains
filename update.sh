#!/bin/sh
set -e

python $1

if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "$(cat .git/COMMIT_EDITMSG)"
fi
