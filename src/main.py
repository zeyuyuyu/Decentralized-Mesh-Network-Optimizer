import networkx as nx
import numpy as np

def optimize_mesh_network(nodes, links):
    """
    Optimizes a decentralized mesh network to improve performance and resilience.
    
    Args:
        nodes (list): List of node objects with attributes like location, capacity, etc.
        links (list): List of link objects with attributes like bandwidth, latency, etc.
    
    Returns:
        G (networkx.Graph): Optimized mesh network graph.
    """
    G = nx.Graph()
    
    # Add nodes to the graph
    for node in nodes:
        G.add_node(node.id, **node.__dict__)
    
    # Add links to the graph
    for link in links:
        G.add_edge(link.source.id, link.target.id, **link.__dict__)
    
    # Apply decentralized optimization algorithm
    for i in range(100):
        for node in G.nodes():
            neighbors = list(G.neighbors(node))
            if len(neighbors) > 0:
                # Compute optimal routing and load balancing
                optimal_routes = compute_optimal_routes(G, node, neighbors)
                update_routing_tables(G, node, optimal_routes)
                balance_load(G, node, neighbors)
    
    return G

def compute_optimal_routes(G, node, neighbors):
    """
    Computes the optimal routes for a node in the mesh network.
    
    Args:
        G (networkx.Graph): The mesh network graph.
        node (str): The ID of the node.
        neighbors (list): List of neighboring node IDs.
    
    Returns:
        optimal_routes (dict): Dictionary mapping neighbor IDs to optimal route metrics.
    """
    optimal_routes = {}
    for neighbor in neighbors:
        # Compute optimal route metrics like latency, bandwidth, etc.
        route_metrics = compute_route_metrics(G, node, neighbor)
        optimal_routes[neighbor] = route_metrics
    return optimal_routes

def update_routing_tables(G, node, optimal_routes):
    """
    Updates the routing table for a node in the mesh network.
    
    Args:
        G (networkx.Graph): The mesh network graph.
        node (str): The ID of the node.
        optimal_routes (dict): Dictionary mapping neighbor IDs to optimal route metrics.
    """
    G.nodes[node]['routing_table'] = optimal_routes

def balance_load(G, node, neighbors):
    """
    Balances the load on a node in the mesh network.
    
    Args:
        G (networkx.Graph): The mesh network graph.
        node (str): The ID of the node.
        neighbors (list): List of neighboring node IDs.
    """
    total_load = sum([G.nodes[neighbor]['load'] for neighbor in neighbors])
    avg_load = total_load / len(neighbors)
    for neighbor in neighbors:
        neighbor_load = G.nodes[neighbor]['load']
        if neighbor_load > avg_load:
            # Offload some traffic to lower-load neighbors
            offload_amount = neighbor_load - avg_load
            G.nodes[neighbor]['load'] -= offload_amount
            for low_load_neighbor in neighbors:
                if G.nodes[low_load_neighbor]['load'] < avg_load:
                    G.nodes[low_load_neighbor]['load'] += offload_amount / (len(neighbors) - 1)
                    break
