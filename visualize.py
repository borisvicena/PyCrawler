import pandas as pd
import networkx as nx
from pyvis.network import Network

# Load data from Excel
filename = 'crawled_data.xlsx'
urls_df = pd.read_excel(filename, sheet_name='URLs')
links_df = pd.read_excel(filename, sheet_name='Links')

# Create a directed graph
G = nx.DiGraph()

# Add nodes (URLs)
for _, row in urls_df.iterrows():
    G.add_node(row['URL'], status=row['Status Code'], error=row['Error'])

# Add edges (links between URLs)
for _, row in links_df.iterrows():
    G.add_edge(row['Source'], row['Target'])

# Create a Pyvis network
net = Network(notebook=True, height='1000px', width='100%', bgcolor='#222222', font_color='white', cdn_resources='in_line')

# Transfer the networkx graph to Pyvis
net.from_nx(G)

# Customize node and edge appearance
for node in net.nodes:
    node['title'] = node['id']
    node['color'] = 'skyblue'
    node['size'] = 10

for edge in net.edges:
    edge['color'] = 'gray'

# Generate the network graph
net.show('crawl_graph.html')

# If running in a notebook, display directly
net.show_buttons(filter_=['physics'])
net.show('crawl_graph.html')
