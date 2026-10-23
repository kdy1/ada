#include "ada.h"

#include <fstream>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

// Fixtures are UTF-8 input URL, TAB, expected serialized URL. Keep validation
// active in Release builds: these checks form part of the measured workload.
int main(int argc, char** argv) {
  if (argc != 2) {
    return 1;
  }
  std::ifstream input(argv[1]);
  std::vector<std::pair<std::string, std::string>> cases;
  std::string line;
  while (std::getline(input, line)) {
    auto tab = line.find('\t');
    if (tab == std::string::npos || tab == 0 || tab + 1 == line.size()) {
      return 2;
    }
    cases.emplace_back(line.substr(0, tab), line.substr(tab + 1));
  }
  if (!input.eof() || cases.empty()) {
    return 3;
  }
  for (unsigned iteration = 0; iteration < 1000; ++iteration) {
    for (const auto& [url, expected] : cases) {
      auto result = ada::parse<ada::url_aggregator>(url);
      if (!result || result->get_href() != expected) {
        std::cerr << "Unexpected URL serialization: " << url << '\n';
        return 4;
      }
    }
  }
  return 0;
}
