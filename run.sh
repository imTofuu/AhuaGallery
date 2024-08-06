#!/usr/bin/env python

if ! test -f ./main.py ; then
  echo "Failed to run. Ensure you are in the main directory of the project."
  exit 0
fi

python3 main.py clear