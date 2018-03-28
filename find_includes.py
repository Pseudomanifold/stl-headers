#!/usr/bin/env python3

import os
import re
import sys

import matplotlib.pyplot as plt
import numpy             as np

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

header_counts        = Counter()
header_cooccurrences = Counter()

for path, directories, files in os.walk(root):
  for name in files:
    filename  = os.path.join(path, name)
    extension = os.path.splitext(filename)[1]
    if extension in extensions:
      headers = process_file(filename)
      headers = process_headers(headers)

      for header1 in headers:
        for header2 in headers:
          if header1 < header2:
            header_cooccurrences[ (header1, header2) ] += 1

      header_counts.update(headers)

labels = []
counts = []
total  = sum(header_counts.values())

# Prepare labels and counts; this ensures that everything is sorted
# according to the counts.
for header, count in header_counts.most_common():
  labels.append(header)
  counts.append(count / total)

print("Dominant headers (accounting for 50% of all usages):")

s = 0.0
for header, count in header_counts.most_common():
  print("  -", header)
  s += count / total

  if s >= 0.50:
    break

########################################################################
# Plot 1: Individual header counts
########################################################################

plt.bar(range(len(labels)), counts, align="center")
plt.xticks(range(len(labels)), labels, rotation="vertical")
plt.show()

########################################################################
# Plot 2: Co-occurrences
########################################################################

header_to_index = dict()

for index, header in enumerate(labels):
  header_to_index[header] = index

cooccurrence_matrix = np.zeros((len(labels), len(labels)))

for (header1,header2),count in header_cooccurrences.most_common():
  u = header_to_index[header1]
  v = header_to_index[header2]

  cooccurrence_matrix[u,v] = count
  cooccurrence_matrix[v,u] = count

plt.matshow(np.log(cooccurrence_matrix+1))
plt.xticks(range(len(labels)), labels, rotation="vertical")
plt.yticks(range(len(labels)), labels)

ax = plt.gca()

# TODO: fix text in cells...
#for (i,j), z in np.ndenumerate(cooccurrence_matrix):
#  ax.text(j, i, '{:0.1f}'.format(z), ha='center', va='center')

plt.show()
