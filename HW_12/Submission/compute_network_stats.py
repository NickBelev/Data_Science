import json
import argparse
import networkx as nx

def compute_network_stats(input_file, output_file):
    # Load the json network
    with open(input_file, 'r', encoding='utf-8') as infile:
        interaction_network = json.load(infile)

    # Instantiate a directed graph using NetworkX
    InteractionGraph = nx.DiGraph()

    # Add edges with weights
    for speaker, listeners in interaction_network.items():
        for listener, intrxn_count in listeners.items():
            InteractionGraph.add_edge(speaker, listener, weight=intrxn_count)

    # degree centrality (unweighted) via library function
    degree_centrality = nx.degree_centrality(InteractionGraph) # what does it return??
    top_degree = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:3]

    # weighted degree centrality (sum of edge weights)
    weighted_degree_centrality = {
        character: sum(data["weight"] for _, _, data in InteractionGraph.edges(character, data=True))
        for character in InteractionGraph.nodes
    }
    top_weighted_degree = sorted(weighted_degree_centrality, key=weighted_degree_centrality.get, reverse=True)[:3] # sort by highest value and take top 3

    closeness_centrality = nx.closeness_centrality(InteractionGraph)
    top_closeness = sorted(closeness_centrality, key=closeness_centrality.get, reverse=True)[:3]

    betweenness_centrality = nx.betweenness_centrality(InteractionGraph, weight='weight')
    top_betweenness = sorted(betweenness_centrality, key=betweenness_centrality.get, reverse=True)[:3]

    # Save the results to a JSON file
    stats = {
        "degree": top_degree,
        "weighted_degree": top_weighted_degree,
        "closeness": top_closeness,
        "betweenness": top_betweenness,
    }

    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(stats, outfile, indent=4)

    print(f"Network statistics saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute network statistics from an interaction network JSON.")
    parser.add_argument("-i", "--input", required=True, help="Path to the input interaction network JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Path to the output statistics JSON file.")

    args = parser.parse_args()
    compute_network_stats(args.input, args.output)

# python3 compute_network_stats.py -i interactions.json -o stats.json