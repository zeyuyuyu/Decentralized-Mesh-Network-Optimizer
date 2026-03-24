import networkx as nx
import numpy as np
import time

class MeshNetworkOptimizer:
    def __init__(self, num_nodes, node_positions, link_capacities):
        self.G = nx.Graph()
        self.num_nodes = num_nodes
        self.node_positions = node_positions
        self.link_capacities = link_capacities
        self.build_network()

    def build_network(self):
        for i in range(self.num_nodes):
            self.G.add_node(i, pos=self.node_positions[i])
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                self.G.add_edge(i, j, capacity=self.link_capacities[i,j])

    def optimize_routing(self, source, destination, bandwidth_demand):
        start_time = time.time()
        path = self.find_shortest_path(source, destination, bandwidth_demand)
        if path is None:
            return None
        self.update_link_capacities(path, bandwidth_demand)
        end_time = time.time()
        print(f'Optimization took {end_time - start_time:.2f} seconds')
        return path

    def find_shortest_path(self, source, destination, bandwidth_demand):
        capacity_map = nx.get_edge_attributes(self.G, 'capacity')
        try:
            path = nx.shortest_path(self.G, source=source, target=destination, weight=lambda u, v, d: 1/max(d['capacity'] - bandwidth_demand, 1e-6))
        except nx.exception.NetworkXNoPath:
            return None
        if not self.path_has_capacity(path, bandwidth_demand):
            return None
        return path

    def path_has_capacity(self, path, bandwidth_demand):
        capacity_map = nx.get_edge_attributes(self.G, 'capacity')
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            if capacity_map[(u, v)] < bandwidth_demand:
                return False
        return True

    def update_link_capacities(self, path, bandwidth_demand):
        capacity_map = nx.get_edge_attributes(self.G, 'capacity')
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            capacity_map[(u, v)] -= bandwidth_demand
            self.G[u][v]['capacity'] = capacity_map[(u, v)]
