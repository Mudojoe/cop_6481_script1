import csv

import matplotlib.pyplot as plt
import networkx as nx


# ########################################
# Spring 2024 Computational Methods in FinTech
# Script 1
# Team 6
# ########################################
#
# #####
# the read_transactions function
#   input : a file name
#   output : the transaction graph as an nx.DiGraph object
#   We use the NetworkX library  to create and work with our directed graph.
#   Function explanation:
#       We call nx.DiGraph() to create our directed graph, "transaction_graph"
#       Then we read the contents of the csv file
#       For each line on the input csv file we connect a weighted, directed edge between
#       the sender and receiver.
#       when finished reading the csv file we retunr the NetworkX grapg to the caller
# #####
def read_transactions(file_name):
    transaction_graph = nx.DiGraph()
    with open(file_name, newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the first row that contains header info
        for row in reader:  # Process each remaining row
            # extract the transaction amount and the sender/receiver from
            # the input line just read
            amount, sender, receiver = float(row[0]), row[1], row[2]
            # use the nx.add_edge call to create an edge with the "amount"
            # the add add_edge() call adds an edge to the graph "transaction_graph"
            # from the node "sender" to the node "receiver",
            # and it associates this edge with some data ... in this case, amount.
            # amount is treated as an attribute of the edge connecting sender to receiver.
            transaction_graph.add_edge(sender, receiver, amount=amount)
    return transaction_graph


#
# #####
# the visualize_network function
#   input : graph - this is the networkx object that contains all
#                   the nodes and edges for from our transactions.cvs file
#           fraud_edges - these are the edges that represent potential
#                   fraud that were detected in the fraud_detection function
#   output : this function output a graph of the transactions.cvs data
def visualize_network(graph, fraud_edges=None):
    # Compute the layout
    if fraud_edges is None:
        fraud_edges = []

    #       compute the layout for the graph using the Kamada-Kawai layout algorithm.
    #       this layout algorithm will position nodes in the graph in an aesthetically pleasing way.
    pos = nx.kamada_kawai_layout(graph)

    # Node sizes based on degree (slightly larger)
    # the alpha value makes the nodes slightly transparent
    degrees = [val for (node, val) in graph.degree()]
    nx.draw_networkx_nodes(graph, pos, node_size=[v * 300 for v in degrees], alpha=0.9)
    # create labels for each node to be added to the graph
    labels = {node: node for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels, font_size=14)

    # differentiate Normal edges from fraud edges
    normal_edges = [(u, v) for u, v in graph.edges() if (u, v) not in fraud_edges]
    # label the non-fraud edges
    normal_edge_labels = {
        (u, v): f"${graph[u][v]['amount']:.2f}" for u, v in normal_edges
    }
    # use the graph , the pos calculated above, draw thw non-fraud edges with a blue color
    nx.draw_networkx_edges(
        graph, pos, edgelist=normal_edges, edge_color="blue", width=1.0
    )

    # now draw the label for the non-fraud edges
    # place the label for the amount slightly above the line for better visibility
    edge_label_pos_offset = -0.075
    for (u, v), label in normal_edge_labels.items():
        x = (pos[u][0] + pos[v][0]) / 2  # Midpoint x-coordinate
        y = (
            pos[u][1] + pos[v][1]
        ) / 2 + edge_label_pos_offset  # Midpoint y-coordinate + offset
        plt.text(
            x, y, label, color="blue", ha="center", va="bottom"
        )  # Adjust the vertical alignment

    # Now draw the Fraud edges
    # Get the list of labels for the fraud edges
    fraud_edge_labels = {
        (u, v): f"${graph[u][v]['amount']:.2f}" for u, v in fraud_edges
    }
    # draw the fraud edges,m slightly thicket and with a red color
    nx.draw_networkx_edges(
        graph, pos, edgelist=fraud_edges, edge_color="red", width=2.0
    )

    # Adjust positions for fraud edge labels (slightly above the line)
    # add the text for the amount to the fraud edges
    for (u, v), label in fraud_edge_labels.items():
        x = (pos[u][0] + pos[v][0]) / 2  # Midpoint x-coordinate
        y = (
            pos[u][1] + pos[v][1]
        ) / 2 + edge_label_pos_offset  # Midpoint y-coordinate + offset
        plt.text(
            x, y, label, color="red", ha="center", va="bottom"
        )  # Adjust the vertical alignment
    # remove axis
    plt.axis("off")
    # render the graph
    plt.show()


#
# #####
# the fraud_detection function
#   input : graph - this is the networkx object that contains all
#                   the nodes and edges for from our transactions.cvs file
#           threshold - any transaction that exceeds this amount will be flagged as
#                    potential fraud. The default is $500.00
#   output : the fraud_edges , this will be used by the visualization function
def fraud_detection(graph, threshold=500.00):
    #   find the list of edges that represent transactions greater
    #       than the threshold
    fraud_edges = [
        (u, v) for u, v in graph.edges() if graph[u][v]["amount"] > threshold
    ]
    #   print the list of fraud edges:   the source person, destination person,
    #       and the transaction amount
    for sender, receiver in fraud_edges:
        amount = graph[sender][receiver]["amount"]
        print(
            f"Potential Fraud Detected (Amount Exceeds $500.00): {sender} -> {receiver}, Amount: ${amount:.2f}"
        )
    #   return the list of fraud edges that were found to caller
    return fraud_edges


#
# #####
# the calculate_degree_centrality function
#   input : graph - this is the networkx object that contains all
#                   the nodes and edges from our csv file
#           N - the number of top users with the highest degree of centrality to be printed
#   output : this function does not return any value but prints the top N users with the highest degree of centrality
#   Function explanation:
#       We call nx.degree_centrality() to calculate the degree centrality of each node in the graph
#       Then we sort the dictionary returned by nx.degree_centrality() in descending order of values
#       Finally, we print the first N items from the sorted dictionary, which represent the top N users with the highest degree of centrality
# #####
def calculate_degree_centrality(graph, N):
    # Calculate the degree centrality of each node
    degree_centrality = nx.degree_centrality(graph)

    # Sort the dictionary by its values in descending order
    sorted_degree_centrality = sorted(
        degree_centrality.items(), key=lambda item: item[1], reverse=True
    )

    # Print the first N items
    for i in range(N):
        print(
            f"User: {sorted_degree_centrality[i][0]}, Degree Centrality: {sorted_degree_centrality[i][1]}"
        )


#
# #####
# the main function
#       step 1 : read in the transactions.cvs file and construct the
#               graph whose nodes are the persons and the directed edges
#               are payments from one person to another
#       step 2 : detect the list of fraud transactions,
#                   this will be the list of edges whose values exceed the
#                   threshold amount. print out this list.
#       step 3 : calculate the degree centrality of each node in the graph and print the top 5 users
#       step 4 : visualize the network using matplotlib.pyplot
#
#
if __name__ == "__main__":
    graph = read_transactions("transactions.csv")
    fraud_edges = fraud_detection(graph, 500.00)
    calculate_degree_centrality(graph, 5)
    visualize_network(graph, fraud_edges)
