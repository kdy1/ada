#!/usr/bin/env bash
set -euo pipefail
engine=$(cd "$1" && pwd)
binary=$2
harness=$(cd "$3" && pwd)
cmake -S "$engine" -B "$engine/build-gungraun" -G Ninja \
  -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=g++-13 \
  -DCMAKE_CXX_FLAGS_RELEASE='-O3 -DNDEBUG -g -gdwarf-4' \
  -DBUILD_SHARED_LIBS=OFF -DADA_TESTING=OFF -DADA_BENCHMARKS=OFF \
  -DADA_TOOLS=OFF -DADA_USE_SIMDUTF=OFF -DADA_USE_UNSAFE_STD_REGEX_PROVIDER=OFF
cmake --build "$engine/build-gungraun" --target ada -j2
g++-13 -std=c++20 -O3 -DNDEBUG -g -gdwarf-4 \
  -I "$engine/include" "$harness/workload.cpp" \
  "$engine/build-gungraun/src/libada.a" -o "$binary"
readelf --sections "$binary" | grep '\.debug_info' > /dev/null
