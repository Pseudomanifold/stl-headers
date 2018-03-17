#!/usr/bin/env python3

import os
import re
import sys

def process_file(filename):
  """
  Extracts the includes from a matching file and returns them as a set
  in order to prevent duplicates.
  """

  re_include = r'\s*#include\s+<([^>]+)>.*'
  headers    = set()

  with open(filename) as f:
    for line in f:
      matches = re.match(re_include, line)
      if matches:
        name = matches.group(1)
        name = name.strip()

        headers.add(name)

  return headers

# List of file extensions that may potentially contain C++ code. This
# should cover most conventional codebases.
extensions = [ ".cc", ".C", ".cxx", ".cpp", ".h", ".hh", ".hxx", ".hpp" ]
root       = sys.argv[1]

for path, directories, files in os.walk(root):
  for name in files:
    filename  = os.path.join(path, name)
    extension = os.path.splitext(filename)[1]
    if extension in extensions:
      process_file(filename)
