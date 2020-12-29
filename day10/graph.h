#ifndef GRAPH_H
#define GRAPH_H
#include <list>
using namespace std;
/*
 * A directed graph using adjacency list representation; every vertex holds a
 * list of all neighbouring vertices that can be reached from it.
 *
 * Each vertex is described by an integer index alone. There is no mapping
 * between index and objects.
 */
class Graph {
public:
    // Construct the graph given the number of vertices...
    Graph(int vertices);
    ~Graph(void);
    // Specify an edge between two vertices.
    void add_edge(int src, int dst);
    // Call the recursive helper function to count all the paths
    unsigned long long int count_paths(int src, int dst);

private:
    const int m_vertices;
    list<int>* m_neighbours;
    void path_counter(int src, int dst, unsigned long long int& path_count);
};
#endif