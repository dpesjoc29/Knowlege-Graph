# 
# 
# 
# 
# just for testing purpose
# 
# 
# 
# 


import networkx as nx

# Create a simple directed graph
G = nx.DiGraph()
G.add_edge("John", "Mary", relationship="related to")
G.add_edge("Alice", "Bob", relationship="friend of")

# Define a question pattern as a subgraph
question_pattern = nx.DiGraph()
question_pattern.add_nodes_from(["subject", "object"])
question_pattern.add_edge("subject", "object", relationship="")

# User's question
user_question = "Who is related to John?"

# Find subgraphs that match the question pattern
matching_subgraphs = []
for subject, obj in G.edges():
    if G[subject][obj]["relationship"] == "related to":
        matching_subgraphs.append({"subject": subject, "object": obj})

# Retrieve answers based on the matching subgraphs
for match in matching_subgraphs:
    subject = match["subject"]
    obj = match["object"]
    relationship = G[subject][obj]["relationship"]

    # Construct and print the answer
    answer = f"{subject} is {relationship} {obj}."
    print(answer)