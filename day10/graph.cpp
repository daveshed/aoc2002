/*
 * C++ program to count all paths from a source to a destination.
 * https://www.geeksforgeeks.org/count-possible-paths-two-vertices/
 * Note that the original example has been refactored.
 */
#include <cassert>
#include <iostream>
#include <list>

#include "graph.h"

using namespace std;

Graph::Graph(int vertices) : m_vertices(vertices)
{
    /* An array of linked lists - each element corresponds to a vertex and will
    hold a list of neighbours...*/
    m_neighbours = new list<int>[vertices];
}

Graph::~Graph(void)
{
    delete[] m_neighbours;
}

void Graph::add_edge(int src, int dst)
{
    m_neighbours[src].push_back(dst);
}

unsigned long long int Graph::count_paths(int src, int dst)
{
    unsigned long long int path_count = 0;
    path_counter(src, dst, path_count);
    return path_count;
}

/*
 * A recursive function that counts all paths from src to dst. Keep track of the
 * count in the parameter.
 */
void Graph::path_counter(int src, int dst, unsigned long long int& path_count)
{
    // If we've reached the destination, then increment count...
    if (src == dst)
    {
        path_count++;
    }
    // ...otherwise recurse into all neighbours...
    else
    {
        for (auto neighbour : m_neighbours[src])
        {
            path_counter(neighbour, dst, path_count);
        }
    }
}
#if 0
// Tests...
int main()
{
    // Create a graph given in the above diagram - see link
    Graph g(5);
    g.add_edge(0, 1);
    g.add_edge(0, 2);
    g.add_edge(0, 3);
    g.add_edge(1, 3);
    g.add_edge(1, 4);
    g.add_edge(2, 3);
    g.add_edge(2, 4);
    // Validate it...
    assert(3 == g.count_paths(0, 3));

    return 0;
}
#endif