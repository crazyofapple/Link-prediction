import sys
from graph import Graph
from utils import evaluate

# here is your result file which will be evaluated
result_file = "../data/result.txt"

# test set you separate from dataset
test_file = "../data/test.txt"

if __name__ == "__main__":
    if len(sys.argv) == 3:
        result_file = sys.argv[1]
        test_file = sys.argv[2]
    elif len(sys.argv) != 1:
        print("Usage: %s <result file> <test file>\n" % sys.argv[0])
        exit(0)
    result_graph = Graph(result_file)
    test_graph = Graph(test_file)
    result_graph.read()
    test_graph.read()
    result_set = set()
    test_set = set()
    result_edge = result_graph.all_edges()
    for a, link in result_edge.items():
        for b in link:
            result_set.add((a, b))
    test_edge = test_graph.all_edges()
    for a, link in test_edge.items():
        for b in link:
            test_set.add((a, b))
    evaluate(test_set, result_set)