#!/usr/bin/env python3

import os
import re
import sys

from collections import Counter

# All system headers defined according to the C++17 standard. This
# should cover most codebases.
system_headers = set( [
  "algorithm", "any", "array", "atomic",
  "bitset",
  "chrono", "codecvt", "complex", "condition_variable",
  "deque",
  "exception", "execution",
  "filsystem", "forward_list", "fstream", "functional", "future",
  "initializer_list", "iomanip", "ios", "iosfwd", "iostream", "istream", "iterator",
  "limits", "list", "locale",
  "map", "memory", "memory_resource", "mutex",
  "new", "numeric",
  "optional", "ostream",
  "queue",
  "random", "ratio", "regex",
  "scoped_allocator", "set", "shared_mutex", "sstream", "stack", "stdexcept", "streambuf", "string", "string_view", "strstream", "system_error",
  "thread", "tuple", "type_traits", "typeindex", "typeinfo",
  "unordered_map", "unordered_set", "utility",
  "valarray", "variant", "vector" ]
)

def process_file(filename):
  """
  Extracts the includes from a matching file and returns them as a set
  in order to prevent duplicates.
  """

  re_include = r'\s*#include\s+[<\"]([^>\"]+)[>\"].*'
  headers    = set()

  with open(filename, encoding='iso8859-1') as f:
    for line in f:
      matches = re.match(re_include, line)
      if matches:
        name = matches.group(1)
        name = name.strip()

        headers.add(name)

  return headers

def process_headers(headers):
  """
  Processes a set of headers by tallying a total count for the
  occurrences of system headers while ignoring all headers that
  have been defined by users.
  """
  headers = [ header for header in headers if header in system_headers ]
  return headers

# List of file extensions that may potentially contain C++ code. This
# should cover most conventional codebases.
extensions = [ ".cc", ".C", ".cxx", ".cpp", ".h", ".hh", ".hxx", ".hpp" ]
root       = sys.argv[1]

header_counts = Counter()

for path, directories, files in os.walk(root):
  for name in files:
    filename  = os.path.join(path, name)
    extension = os.path.splitext(filename)[1]
    if extension in extensions:
      headers = process_file(filename)
      headers = process_headers(headers)

      header_counts.update(headers)

print(header_counts.most_common(10))
