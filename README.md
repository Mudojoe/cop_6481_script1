# cop6481_script_1
Spring 2024 Computational Methods in FinTech 
<br>
** Script 1 Team6**
 


## Transaction Network Analysis

### Problem Statement:

In a financial transaction network<br>
* each node represents a user, and 
* each directed edge represents a financial transaction from one user to another. 

Write a Python program to perform the following tasks:
* Load Data:<br>
    Read a CSV file containing transaction data.<br>
    The CSV file should have two columns: 'sender' and 'receiver,'<br>
    representing the sender and receiver of each transaction.<br>
    You can create your data file with 10-15 users(nodes).<br>
**_Note:_**<br>

        Our .csv file is called transaction. 
        It contains 3 columns, the required 'sender' and 'receiver' columns and  
        a 3rd column called amount. 
        Our program will use the 'Amount' column to satisfy the 
        some of the additional requirements, below. 

* Build a Graph:<br>
  Create a directed graph where nodes represent users and edges represent transactions.<br>
**_Note:_**<br>

        The column 'Amount. 
        Is used as the value (weight) on the edge between two nodes and 
        represents the value of a payment from one person (the source node) to
        another (the destination node)

* Detect Fraudulent Transactions:
  Implement a function to detect potentially fraudulent transactions.<br> 
  You can define fraud based on a certain threshold of transaction amounts or <br>
  other relevant criteria.Print the details of any detected fraudulent transactions,<br>
  including the sender, receiver, and transaction amount.<br>
**_Note:_**<br>

        We defined potential fraud (or money laundering) as any payment amount 
        over $50.00.

* Calculate Degree Centrality: (Bonus - 5 points)<br>
  Implement a function to calculate the degree of centrality<br>
  of each user in the network.<br>
  Print the top N users with the highest degree of centrality.

* Visualize the Transaction Network:<br>
  Use a graph visualization library (e.g., NetworkX, Matplotlib)<br>
  to visualize the transaction network.


## Running the program

The entire code is contained in file <br>
"network_transactions.py"
To run the program simply run this file.
