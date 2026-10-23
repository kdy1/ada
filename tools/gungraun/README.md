# Fork Gungraun measurements

This fork-only harness measures `ada::parse<ada::url_aggregator>` on seven fixed
UTF-8 fixture sets: ASCII, paths, percent encoding, IDNA, IPv4, IPv6, and opaque
URLs. Each fixture contains an input URL and its expected serialization,
separated by one tab. The native executable runs 1000 iterations and checks
every result, including in Release builds. It measures the whole process,
including startup, file reading, parsing, result validation, and teardown.
These cases do not cover setters, relative resolution, URLPattern, search params,
all invalid inputs, or all production traffic.

The pinned Rust 1.95.0 / Gungraun 0.20.0 binary driver launches an unstripped
GCC 13 executable on Ubuntu 24.04. CMake builds a static Release library with
`-O3 -DNDEBUG -g -gdwarf-4`, without simdutf, regex, tests or benchmark dependencies.
The workflow fixes the harness checkout and executable path for both revisions.
It rebuilds each exact full SHA independently. Record the runner image and
compiler/Valgrind versions from metadata; do not combine different environments.

Run in `kdy1/ada` after the workflow lands on its default branch:

```sh
gh workflow run gungraun.yml --repo kdy1/ada --ref main \
  -f base_ref=<full-base-sha> -f head_ref=<full-head-sha>
```

The optional `filter` selects a literal substring of case IDs. `workloads` is a
JSON array of TSV paths inside the workflow checkout. Defaults select all seven
fixtures. Freeze workload hashes, cases, workflow SHA and frequencies before
changing production code. Frequencies are 1 each because production frequencies
are unknown. All selected cases are protected against regressions of 1% or more.

Artifacts `gungraun-<run-id>-<attempt>` contain metadata, exact binaries, CMake
caches, raw profiles, self/inclusive annotations, runner logs, schema-7 summaries
and comparison results. Retention is 30 days. Only `status: complete` is evidence
of a successful comparison. A same-SHA comparison must produce identical Ir for
every case; it verifies infrastructure and does not establish an optimization.

`report.py` rejects incomplete or nonpositive measurements. Its standard gate
requires a portfolio Ir reduction of at least 1% and individual regressions below
1%, using equal frequencies. A valid measurement job remains green if this gate
fails. Ir counts instructions and does not measure elapsed time. Correctness
tests and human approval are separate requirements for upstream publication.

Validate harness changes with:

```sh
python3 -m unittest discover -s tools/gungraun -p 'test_*.py'
cargo bench --locked --manifest-path tools/gungraun/Cargo.toml --no-run
bash -n tools/gungraun/build.sh
actionlint .github/workflows/gungraun.yml
bash tools/run-clangcldocker.sh
```

The design adapts the pinned [PrimJS fork harness](https://github.com/kdy1/primjs/tree/dcb6d7bc964791577e9db3be8e777c27e5e209af/tools/gungraun),
using the [Gungraun binary benchmark API](https://gungraun.github.io/gungraun/latest/html/benchmarks/binary_benchmarks/quickstart.html).
