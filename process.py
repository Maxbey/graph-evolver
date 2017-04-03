import csv
from collections import OrderedDict
from decimal import Decimal

from igraph import Graph

from factrories import VertexFactory
from rules.non_linear_prefer_binding import NonLinearPreferBindingRule


class Process(object):
    def __init__(self, graph_initial_size, distribution, steps_count,
                 output_filename):
        self.graph_initial_size = graph_initial_size
        self.distribution = distribution
        self.steps_count = steps_count
        self.output_filename = output_filename

    def process_evolve(self):
        self.graph = Graph(directed=False)
        self.fill_graph()

        evolver = NonLinearPreferBindingRule(
            lambda item: float(item),
            self.distribution, VertexFactory()
        )

        evolver.evolve(self.graph, self.steps_count)

        degrees = self.get_vertex_digrees()
        sorted_degrees = OrderedDict(
            sorted(degrees.items(), key=lambda item: int(item[0]))
        )

        vcount = self.graph.vcount()
        ecount = self.graph.ecount()

        with open(self.output_filename, 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([vcount, ecount])
            writer.writerow(['', ''])

            for key, value in sorted_degrees.iteritems():
                empirical_distr = Decimal(value) / Decimal(vcount) \
                    if value else 0

                writer.writerow([key, value, empirical_distr])

    def fill_graph(self):
        for vertex in range(1, self.graph_initial_size + 1):
            self.graph.add_vertex(-vertex)

        for source_vertex in self.graph.vs:
            for target_vertex in self.graph.vs:
                if source_vertex == target_vertex:
                    continue

                try:
                    if self.graph.es.select(
                            _source=source_vertex.index,
                            _target=target_vertex.index
                    ):
                        continue

                    if self.graph.es.select(
                            _source=target_vertex.index,
                            _target=source_vertex.index
                    ):
                        continue
                except ValueError:
                    pass

                self.graph.add_edge(source_vertex, target_vertex)

    def get_vertex_digrees(self):
        degree_entries = {}
        max_degree = self.graph.maxdegree()

        for degree in range(0, max_degree + 1):
            degrees = [d for d in self.graph.vs.degree() if d == degree]
            count = len(degrees)

            degree_entries[str(degree)] = count

        return degree_entries
