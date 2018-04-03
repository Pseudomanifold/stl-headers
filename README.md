# An analysis of STL headers in large C++ projects

The main script of this project requires a directory that contains
multiple git repositories of C++ code. To get a list of worthwhile
picks, you can either pick them yourself or use a script:

    $ ./get_trending_repositories.sh

This script uses `curl` to query the GitHub search to return *all*
trending C++ repositories of the last month.

Assuming that you placed the repositories in a folder `repos`, you
can perform an analysis of the headers by calling the main script:

    $ ./header_analysis.py repos

This will create SVG files in the current directory.

# Examples

The following visualizations have been created by analysing the
following projects:

- [Electron](https://github.com/electron/electron)
- [RethinkDB](https://github.com/rethinkdb/rethinkdb)
- [Swift](https://github.com/apple/swift)
- [TensorFlow](https://github.com/tensorflow/tensorflow)

![Histogram](/Examples/stl_headers_histogram.svg?raw=true "Histogram")

![Matrix](/Examples/stl_headers_cooccurrences.svg?raw=true "Matrix")
