import random
import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import simpledialog, messagebox
from math import log

class PPI:
    def __init__(self):
        # Load proteins from file, ensuring names are 1 to 7 characters and distinct
        self.proteins = self.load_proteins_from_file('Proteins.txt')
        #self.proteins = self.load_proteins_from_file('names_prot.txt')
        self.G = nx.Graph()
        self.G.add_nodes_from(self.proteins)

    def load_proteins_from_file(self, file_path):
        with open(file_path, 'r') as file:
            protein_names = file.read().splitlines()
        
        # Ensure protein names are distinct
        distinct_proteins = set(protein_names)
        return list(distinct_proteins)
    
        """# Ensure protein names are 1 to 7 characters and distinct
        distinct_proteins = set()
        for name in protein_names:
            if 1 <= len(name) <= 7:
                distinct_proteins.add(name)
        return list(distinct_proteins)"""

    def get_user_input(self, prompt, minvalue, maxvalue):
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        user_input = simpledialog.askinteger("Input", prompt, minvalue=minvalue, maxvalue=maxvalue)
        root.destroy()  # Close the dialog window
        return user_input

    def get_protein_input(self, prompt):
        while True:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            protein = simpledialog.askstring("Input", prompt, parent=root)
            root.destroy()  # Close the dialog window
            
            if protein in self.proteins:
                return protein
            else:
                messagebox.showerror("Error", "Invalid protein name entered. Please try again.")


    def create_graph(self, number_of_interactions):
        # Create a new graph instance
        self.G = nx.Graph()
        self.G.add_nodes_from(self.proteins)

        # Create a minimum spanning tree to ensure initial connectivity
        mst = nx.minimum_spanning_tree(nx.complete_graph(self.proteins))
        self.G.add_edges_from(mst.edges())

        # Add additional edges if needed, without exceeding the specified number
        while self.G.number_of_edges() < number_of_interactions:
            protein1, protein2 = random.sample(self.proteins, 2)
            if not self.G.has_edge(protein1, protein2):
                self.G.add_edge(protein1, protein2)

        # If the graph has more edges than needed, remove random edges
        while self.G.number_of_edges() > number_of_interactions:
            edge_to_remove = random.choice(list(self.G.edges()))
            self.G.remove_edge(*edge_to_remove)

        # Save the interactions to a file
        with open('Proteins_interaction.txt', 'w') as file:
            for edge in self.G.edges():
                file.write(f"{edge[0]} - {edge[1]}\n")

    def Dist(self, source, target):
        try:
            distance = nx.dijkstra_path_length(self.G, source=source, target=target)
            return distance
        except nx.NetworkXNoPath:
            return None

    def draw_graph(self):
        plt.figure(figsize=(8, 5))
        nx.draw(self.G, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700)
        plt.show()

    def calculate_characteristic_path_length(self):
        if nx.is_connected(self.G):
            total_distance = sum(nx.dijkstra_path_length(self.G, source, target)
                                for source in self.proteins for target in self.proteins if source != target)
            num_pairs = len(self.proteins) * (len(self.proteins) - 1)
            L = total_distance / num_pairs
            return L
        else:
            return None

    def is_small_world(self):
        # Calculate the average shortest path length (characteristic path length)
        if nx.is_connected(self.G):
            avg_shortest_path_length = nx.average_shortest_path_length(self.G)
        else:
            return "The graph is not connected, which is a prerequisite for a small-world network."

        # Calculate the clustering coefficient
        clustering_coefficient = nx.average_clustering(self.G)

        # Small-world networks typically have a diameter less than or equal to 6
        diameter = nx.diameter(self.G)

        # Check if the network has small-world characteristics
        if avg_shortest_path_length < log(len(self.proteins)) and clustering_coefficient > 0.5 and diameter <= 6:
            return True
        else:
            return False

    def calculate_degree(self, node):
        if node in self.G:
            return self.G.degree(node)
        else:
            return None

    def calculate_clustering_coefficient(self):
        return nx.average_clustering(self.G)

    def edge_betweenness(self):
        return nx.edge_betweenness_centrality(self.G)

    def visualize_graph(self, source=None, target=None, highlight_node=None):
        # Draw the graph with Matplotlib
        pos = nx.spring_layout(self.G)  # positions for all nodes
        plt.figure(figsize=(12, 8))

        # Calculate edge betweenness centrality
        edge_betweenness = self.edge_betweenness()

        # Normalize edge betweenness centrality values for visualization
        min_betweenness = min(edge_betweenness.values())
        max_betweenness = max(edge_betweenness.values())
        normalized_betweenness = {edge: (value - min_betweenness) / (max_betweenness - min_betweenness) 
                                for edge, value in edge_betweenness.items()}

        # Draw edges
        nx.draw_networkx_edges(self.G, pos, width=1.0, alpha=0.5)

        # Draw nodes
        nx.draw_networkx_nodes(self.G, pos, node_size=700, node_color='lightblue', label='Nodes')

        # Draw labels
        nx.draw_networkx_labels(self.G, pos, font_size=20, font_family='sans-serif')

        # Highlight the source and target nodes with circles
        if source and target:
            nx.draw_networkx_nodes(self.G, pos, nodelist=[source, target], node_size=700, node_color='green', label='Source/Target Nodes')
            
            # Draw discontinued circles around the source and target nodes
            source_circle = plt.Circle(pos[source], 0.15, color='black', fill=False, linewidth=2, linestyle='dashed')
            target_circle = plt.Circle(pos[target], 0.15, color='black', fill=False, linewidth=2, linestyle='dashed')
            plt.gca().add_patch(source_circle)
            plt.gca().add_patch(target_circle)

            # Add labels for the source and target nodes near the circles
            plt.text(pos[source][0], pos[source][1] + 0.1, 'source', fontsize=12, color='black', horizontalalignment='center')
            plt.text(pos[target][0], pos[target][1] + 0.1, 'target', fontsize=12, color='black', horizontalalignment='center')

            # Highlight the shortest path with a horizontal line
            path = nx.shortest_path(self.G, source=source, target=target)
            path_edges = list(zip(path, path[1:]))
            nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='red', width=2, style='solid', label='Shortest Path')

        # Highlight the node with its degree
        if highlight_node:
            nx.draw_networkx_nodes(self.G, pos, nodelist=[highlight_node], node_size=700, node_color='orange', label='Highlighted Node')
            nx.draw_networkx_edges(self.G, pos, edgelist=self.G.edges(highlight_node), edge_color='orange', width=2, label='Node Edges')

        # Show the colorbar for edge betweenness
        sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=min_betweenness, vmax=max_betweenness))
        sm._A = []
        plt.colorbar(sm, label='Edge Betweenness Centrality')

        # Draw edge betweenness values as colored text
        for edge, centrality in normalized_betweenness.items():
            x = (pos[edge[0]][0] + pos[edge[1]][0]) / 2
            y = (pos[edge[0]][1] + pos[edge[1]][1]) / 2
            plt.text(x, y, f"{centrality:.2f}", fontsize=10, color=plt.cm.viridis(centrality),
                    horizontalalignment='center', verticalalignment='center')

        # Calculate the shortest distance and include it in the title
        shortest_distance = nx.shortest_path_length(self.G, source, target) if source and target else 'N/A'

        # Additional metrics
        clustering_coefficient = self.calculate_clustering_coefficient()

        # Show the results on the figure
        plt.title(   r"$\bf{{Protein-Protein\ Interaction\ Network}}$" + '\n'  # Bold 
                f"\nShortest Distance from {source} to {target} = {shortest_distance}\n"
                f"Characteristic Path Length = {self.calculate_characteristic_path_length():.2f}\n"
                f"Clustering Coefficient = {clustering_coefficient:.2f}\n"
                f"Small-World: {'Yes' if self.is_small_world() else 'No'}\n"
                f"Degree of Node '{highlight_node}' = {self.G.degree(highlight_node) if highlight_node else 'N/A'}",
                size=15,loc='center' )
        plt.legend()
        plt.tight_layout()
        plt.show()

    def run(self):
        max_interactions = (len(self.proteins) * (len(self.proteins) - 1)) // 2
        number_of_interactions = self.get_user_input(
            f"Enter the number of interactions (between 2 and {max_interactions}):", 2, max_interactions)
        
        self.create_graph(number_of_interactions)
        self.draw_graph()

        source_protein = self.get_protein_input("Enter the source protein:")
        target_protein = self.get_protein_input("Enter the target protein:")
        
        while source_protein == target_protein:
            messagebox.showerror("Error", "Source and target proteins cannot be the same. Please enter different names.")
            source_protein = self.get_protein_input("Enter the source protein:")
            target_protein = self.get_protein_input("Enter the target protein:")

        if source_protein and target_protein:
            shortest_distance = self.Dist(source_protein, target_protein)
            if shortest_distance is not None:
                messagebox.showinfo("Shortest Distance", f"The shortest distance from {source_protein} to {target_protein} = {shortest_distance}")
            else:
                messagebox.showerror("No Path", "There is no path between the selected proteins.")
        
        L = self.calculate_characteristic_path_length()
        if L is not None:
            messagebox.showinfo("Characteristic Path Length", f"The characteristic path length of the network is: {L:.2f}")
        else:
            messagebox.showerror("Disconnected Graph", "The graph is not connected, so the characteristic path length cannot be calculated.")

        # Check if the network is a small-world network
        small_world_status = self.is_small_world()
        if small_world_status:
            messagebox.showinfo("Small-World Status", "The network is a small-world network.")
        else:
            messagebox.showinfo("Small-World Status", "The network is not a small-world network.")

        # Prompt the user for the node to calculate its degree
        node_name = self.get_protein_input("Enter the name of the node (Noeud) to calculate its degree:")
        if node_name:
            node_degree = self.calculate_degree(node_name)
            if node_degree is not None:
                messagebox.showinfo("Node Degree", f"The degree of node {node_name} =  {node_degree}")
            else:
                messagebox.showerror("Error", f"The node {node_name} does not exist in the graph.")

        # Visualize the graph with all results
        self.visualize_graph(source_protein, target_protein, highlight_node=node_name)

# Create an instance of the PPI class and run it
ppi = PPI()
ppi.run()
