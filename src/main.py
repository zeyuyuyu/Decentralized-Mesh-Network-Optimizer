import networkx as nx
import numpy as np

def optimize_mesh_network(nodes, links):
    """
    Optimizes a decentralized mesh network by minimizing the overall network latency.

    Args:
        nodes (list): List of node objects with properties like location, capacity, etc.
        links (list): List of link objects with properties like bandwidth, latency, etc.

    Returns:
        networkx.Graph: Optimized mesh network graph.
    """
    G = nx.Graph()

    # Add nodes to the graph
    for node in nodes:
        G.add_node(node.id, **node.__dict__)

    # Add links to the graph
    for link in links:
        G.add_edge(link.source.id, link.target.id, **link.__dict__)

    # Apply optimization algorithm
    routing_table = _optimize_routing(G)

    return G, routing_table

def _optimize_routing(G):
    """
    Optimizes the routing table for the mesh network using a decentralized algorithm.

    Args:
        G (networkx.Graph): The mesh network graph.

    Returns:
        dict: Optimized routing table mapping node IDs to next hop node IDs.
    """
    routing_table = {}

    for node in G.nodes:
        # Find the best next hop for each destination node
        best_next_hop = _find_best_next_hop(G, node)
        routing_table[node] = best_next_hop

    return routing_table

def _find_best_next_hop(G, source_node):
    """
    Finds the best next hop for a given source node in the mesh network.

    Args:
        G (networkx.Graph): The mesh network graph.
        source_node (str): The ID of the source node.

    Returns:
        str: The ID of the best next hop node.
    """
    best_next_hop = None
    min_latency = float('inf')

    for neighbor in G.neighbors(source_node):
        path_latency = sum(d['latency'] for u, v, d in nx.shortest_path(G, source=source_node, target=neighbor, weight='latency'))
        if path_latency < min_latency:
            min_latency = path_latency
            best_next_hop = neighbor

    return best_next_hop
