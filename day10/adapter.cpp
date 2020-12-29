#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <vector>

#include "graph.h"

#define INPUT_FILENAME    "input-day10.txt"

const std::vector<int> example_adapters1{16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4};
const std::vector<int> example_adapters2 \
    {28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1,
     32, 25, 35, 8 , 17, 7 , 9 , 4 , 2 , 34, 10, 3 };

std::vector<int> read_ints(std::istream& input);
std::vector<int> get_joltage_levels(const std::vector<int>& adapters);
std::vector<int> joltage_differences(const std::vector<int>& adapters);
int count_accessible_joltages(
    const std::vector<int>& joltages, int idx);
void show_joltages(const std::vector<int>& joltages);
int get_solution_part1(const std::vector<int>& adapters);
int get_solution_part2(const std::vector<int>& adapters);

// read ints line by line from a stream
std::vector<int> read_ints(std::istream& input)
{
    std::vector<int> result;
    while (!input.eof())
    {
        std::string line;
        getline(input, line);
        try {
            result.push_back(std::stoi(line, nullptr));
        }
        catch (std::invalid_argument) {
            std::cout << "Couldn't parse <" << line << ">" << std::endl;
        }
    }
    return result;
}

std::vector<int> get_joltage_levels(const std::vector<int>& adapters)
{
    // copy...
    std::vector<int> joltage_levels(adapters);
    // sort...
    std::sort(joltage_levels.begin(), joltage_levels.end());
    // add on the outlet and device joltages...
    int outlet_jolts = 0;
    int device_jolts = *(joltage_levels.end() - 1) + 3;
    joltage_levels.insert(joltage_levels.begin(), outlet_jolts);
    joltage_levels.push_back(device_jolts);
    return joltage_levels;
}

// put in your sorted joltages...
std::vector<int> joltage_differences(const std::vector<int>& joltage_levels)
{
    // std::vector<int> joltage_levels = get_joltage_levels(adapters);
    // get differences...
    std::vector<int> deltas;
    for (
        auto jolts = joltage_levels.begin();
        jolts != (joltage_levels.end() - 1);
        jolts++)
    {
        int delta = *(jolts + 1) - *jolts;
        deltas.push_back(delta);
    }
    assert(deltas.size() == (joltage_levels.size() - 1));
    return deltas;
}

// joltages must be sorted first...
int count_accessible_joltages(
    const std::vector<int>& joltages, int idx)
{
    // return early if we are looking at the last element...
    bool last_element = (idx + 1) == joltages.size();
    if (last_element)
    {
        return 0;
    }
    // Look at following elements and store until the difference is too big...
    int next_idx = idx + 1;
    int count = 0;
    while (
        ((joltages[next_idx] - joltages[idx]) <= 3)
        && next_idx < joltages.size())
    {
        count++;
        next_idx++;
    }
    return count;
}

// joltages must be sorted first...
std::vector<int> get_accessible_joltages(
    const std::vector<int>& joltages, int idx)
{
    std::vector<int> result;
    // return early if we are looking at the last element...
    bool last_element = (idx + 1) == joltages.size();
    if (last_element)
    {
        return result;
    }
    // Look at following elements and store until the difference is too big...
    int next_idx = idx + 1;
    while (
        ((joltages[next_idx] - joltages[idx]) <= 3)
        && next_idx < joltages.size())
    {
        result.push_back(joltages[next_idx]);
        next_idx++;
    }
    return result;
}

// joltages must be sorted here...
Graph make_joltage_graph(const std::vector<int>& levels)
{
    // std::cout << "Building graph..." << std::endl;
    Graph graph(levels.back());
    // iterate over each joltage level...
    for (int i = 0; i < levels.size(); i++)
    {
        // find the accessible joltages and create edges to represent them.
        // note that there will be unconnected vertices in the graph that can be
        // ignored.
        for (auto joltage : get_accessible_joltages(levels, i))
        {
            graph.add_edge(levels[i], joltage);
        }
    }
    // std::cout << "Built graph." << std::endl;
    return graph;
}

// count paths between two levels (not indices)
unsigned long long int count_paths_between(
    const std::vector<int>& levels, int src, int dst)
{
    return make_joltage_graph(levels)
            .count_paths(src, dst);
}

int get_solution_part1(const std::vector<int>& adapters)
{
    std::vector<int> differences = \
        joltage_differences(get_joltage_levels(adapters));
    int count_1_jolts = 0;
    int count_3_jolts = 0;
    for (auto difference : differences)
    {
        switch (difference)
        {
            case 1:
                count_1_jolts++;
                break;
            case 2:
                break;
            case 3:
                count_3_jolts++;
                break;
            default:
                throw std::runtime_error("Unacceptable joltage difference");
        }
    }
    return count_1_jolts * count_3_jolts;
}

int get_solution_part2(const std::vector<int>& adapters)
{
    /*1. sort the adapters, prepend the wall and append the device joltage...*/
    std::vector<int> levels = get_joltage_levels(adapters);
    /* 2. find the differences between each joltage level...*/
    std::vector<int> deltas = joltage_differences(levels);
    /* 3. Don't count all the paths! We only need to count until we reach a
          delta of 3. This truncates the graph. Then we can build another graph
          and carry on counting from there. */
    unsigned long long int paths = 1U;  // Really big!
    int src = 0;
    int dst = 0;
    while (dst < deltas.size())
    {
        while (deltas[dst] < 3)
        {
            dst++;
        }
        std::cout << "Counting paths " << levels[src] << " -> "  \
            << levels[dst] << std::endl;
        paths *= count_paths_between(levels, levels[src], levels[dst]);
        std::cout << "Paths = " << paths << std::endl;
        src = dst;
        dst++;
    }
    return paths;
}

void show_joltages(const std::vector<int>& joltages)
{
    for (auto jolts : joltages)
    {
        std::cout << jolts << std::endl;
    }
}

int main(void)
{
    // test against examples...
    assert(35 == get_solution_part1(example_adapters1));
    assert((22 * 10) == get_solution_part1(example_adapters2));
    assert(8 == get_solution_part2(example_adapters1));
    assert(19208 == get_solution_part2(example_adapters2));

    std::ifstream input(INPUT_FILENAME);
    assert(input.is_open());
    std::vector<int> problem_input = read_ints(input);
    input.close();
    // solution part1...
    std::cout \
        << "PART1: solution..." \
        << get_solution_part1(problem_input) \
        << std::endl;

    // solution part2...
    std::cout \
        << "PART2: solution..." \
        << get_solution_part2(problem_input) \
        << std::endl;
    return 0;
}