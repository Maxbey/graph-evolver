import random


class NonLinearPreferBindingRule(object):
    def __init__(self, binding_rule, probability_ranges,
                 vertex_factory):
        self.vertex_layers = {}

        self.binding_rule = binding_rule
        self.propability_ranges = probability_ranges
        self.vertex_factory = vertex_factory

    def evolve(self, graph, step):
        for vertex in list(graph.vs):
            self.add_vertex_to_layer(vertex, vertex.degree())

        for i in range(step):
            vertices = []
            new_vertex = self.vertex_factory.create()

            rand_range = random.uniform(0, 1)
            s = 0.0
            edges_to_add = 0

            for j in range(len(self.propability_ranges)):
                s += self.propability_ranges[j]

                if s > rand_range:
                    edges_to_add = j
                    break

            while True:
                rand_layer = self.vertex_layers.get(self.get_layer())
                rand_vertex = random.choice(rand_layer)

                vertices.append(rand_vertex)

                if len(vertices) == edges_to_add:
                    break

            graph.add_vertex(new_vertex)
            new_vertex = graph.vs[len(graph.vs) - 1]
            for v in vertices:
                vertex_degree = v.degree()
                graph.add_edge(new_vertex, v)
                vertex_layer = self.vertex_layers.get(str(vertex_degree))
                vertex_layer.pop(vertex_layer.index(v))

                if not len(vertex_layer):
                    self.vertex_layers.pop(str(vertex_degree))

                self.add_vertex_to_layer(
                    v, vertex_degree + 1
                )
            self.add_vertex_to_layer(new_vertex, str(edges_to_add))

    def add_vertex_to_layer(self, vertex, degree):
        layer = self.vertex_layers.get(str(degree), None)

        if layer is None:
            layer = self.vertex_layers[str(degree)] = []

        if vertex not in layer:
            layer.append(vertex)

    def get_layer(self):
        k, tr = 0, 0.0
        summ = 0.0
        rand_range = random.uniform(0, 1)

        def get_layer_size(degree):
            return len(self.vertex_layers.get(degree))

        for layer_degree in self.vertex_layers:
            layer_size = get_layer_size(layer_degree)

            summ += self.binding_rule(int(layer_degree)) * layer_size

        for ld in self.vertex_layers:
            ls = get_layer_size(ld)
            tr += float(ls) * float(
                self.binding_rule(int(ld))) / summ

            if rand_range < tr:
                return ld
