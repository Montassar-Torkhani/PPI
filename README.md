
# Protein-Protein Interaction Network 

## Description

This Python script facilitates the analysis of Protein-Protein Interaction (PPI) networks. It offers functionalities for:

- **Loading Protein Data:** Load protein names from a text file.
- **Network Creation:** Construct a PPI network with user-specified interaction count.
- **Visualization:** Generate a visual representation of the network using Matplotlib.
- **Shortest Path Calculation:** Determine the shortest distance between two proteins in the network.
- **Network Properties:** Calculate various network properties like characteristic path length and small-world network classification.
- **Degree Calculation:** Compute the degree (number of connections) of a specific protein.
- **Interactive User Input:** Employ tkinter for user-friendly interaction to specify parameters and request protein names.


## Features

- User-friendly interface through tkinter for input and visualization.
- Comprehensive network analysis with various metrics.
- Customizable network creation based on user-defined interaction count.



## Screenshots

- **Input Number of Interactions
![input_interaction](https://github.com/Montassar-Torkhani/Xamarin-Project/assets/97996083/ae3b6584-6510-498d-ad07-54df7655737c)


- **Result of PPI Network
![ProtNetwork](https://github.com/Montassar-Torkhani/Xamarin-Project/assets/97996083/a06270fa-e3da-4428-ab31-f595bc278508)


- **Input Protein Source
![ptsSurce](https://github.com/Montassar-Torkhani/Xamarin-Project/assets/97996083/00ff1f78-b63f-48b0-959a-fb65036bb0a9)


- **Input Protein Target
![ptTarget](https://github.com/Montassar-Torkhani/Xamarin-Project/assets/97996083/119b66be-0673-43d0-ac10-47c868424da6)


- **Input Protein for Degree Calculation
![deg noeud](https://github.com/Montassar-Torkhani/Xamarin-Project/assets/97996083/6d8b0359-3465-4e03-b45d-0a1817b23cd4)


- **Result of Protein-Protein Interaction Network :
- Shortest Distance from Source to Target: {Shortest Distance Value}
- Characteristic Path Length: {Characteristic Path Length Value}
- Clustering Coefficient: {Clustering Coefficient Value}
- Small-World: {Yes/No}
- Degree of Node 'Protein': {Degree Value}
- Edge Betweenness Centrality : {the values of edge betweenness centrality of each pair of nodes}


*![result_PPI](https://github.com/Montassar-Torkhani/Xamarin-Project/assets/97996083/43ddea08-6bc4-4197-a134-c1a7f05d572c)


## Usage

### Option 1: Using Anaconda

1. **Install Anaconda:**
   - Download and install Anaconda for your operating system from the official website: [Anaconda](https://www.anaconda.com/download).
   - Choose the appropriate installer based on your system (Windows, macOS, or Linux).
   - Consider adding Anaconda to your system's PATH environment variable for easier access to commands during installation.

2. **Create a New Environment (Optional but Recommended):**
   - Anaconda environments allow you to manage different Python versions and their dependencies without conflicts. Here's how to create a new environment named `ppi_env` for this project:
   ```bash
   conda create -n ppi_env python=3.11.5

3. **Activate the environment to use it:**
*conda activate ppi_env

4. **Install Dependencies:**
-Inside the activated environment (if you created one), install the required libraries using pip:
*pip install networkx matplotlib tkinter

5. **Install Dependencies:**
- Navigate to the project directory using your terminal and execute the script:
*python PPi.py

