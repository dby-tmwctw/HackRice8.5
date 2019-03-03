# graph = {1:2, 3:4, 5:6}
company_graph = {'Apple':'AAPL', 'Amazon':'AMZN', 'Facebook':'FB', 'Google':'GOOGL',
                 'Microsoft':'MSFT', 'Intel':'INTC', 'Adobe':'ADBE', 'SAP':'SAP','Sony':'SNE', 'Oracle':'ORCL', 'Tesla':'TSLA', 'Alibaba':'BABA', 'Baidu':'BIDU'}

def read_graph(filename):
    """
    Read a graph from a file.  The file is assumed to hold a graph
    that was written via the write_graph function.

    Arguments:
    filename -- name of file that contains the graph

    Returns:
    The graph that was stored in the input file.
    """
    with open(filename) as f:
        g = eval(f.read())
    return g

def write_graph(g, filename):
    """
    Write a graph to a file.  The file will be in a format that can be
    read by the read_graph function.

    Arguments:
    g        -- a graph
    filename -- name of the file to store the graph

    Returns:
    None
    """
    with open(filename, 'w') as f:
        f.write(repr(g))

# write_graph(graph, 'try_graph.repr')
# print (read_graph('try_graph.repr'))
write_graph(company_graph, 'company_graph.repr')
