import requests
from bs4 import BeautifulSoup
# import nltk
# from nltk.tokenize import sent_tokenize
import spacy
import matplotlib.pyplot as plt
import networkx as nx


# nltk.download('punkt')
nlp = spacy.load('en_core_web_sm')

articles  = [
        {"url" :"https://thehimalayantimes.com/kathmandu/police-arrest-two-more-persons-in-fake-academic-certificate-case", "title": "Fake Academic Certificate Case"},
        {"url" :"https://thehimalayantimes.com/world/dengue-outbreak-in-bangladesh-sparks-alarm-after-364-people-die-this-year-and-infections-rise", "title": "Dengue outbreak in Bangladesh"},
        {"url" :"https://thehimalayantimes.com/nepal/forest-should-be-made-a-source-of-income-says-oli", "title": "Forest as income says KP Oli"}
]


#initialize a directed graoh
G = nx.DiGraph()


for article in articles:
    article_url = article["url"]
    article_title = article["title"]

    article_response = requests.get(article_url)
    article_content = article_response.content
    article_soup = BeautifulSoup(article_content, 'html.parser')

    # print("test_1")

    #finding article content
    article_text = article_soup.find('div', class_= 'ht-article-details')
    # print("test_2")
    

    if article_text:
        #extrating text from article content
        article_text = article_text.get_text()
        # print("test_3")
    

        #process text using spacy
        doc = nlp(article_text)
    

        #printing sentences 
        # print(f"Processed sentences from '{article_title}':")
        
        #process each sentences
        for sent in doc.sents:
            # print("Sentence:", sent)
            subject = None
            obj = None
            relationship = None

            #iterating through tokens and identify subjects, objects and relationship using modifiers
            for token in sent:
                if "subj" in token.dep_:
                    subject = token.text
                elif "obj" in token.dep_:
                    obj = token.text
                elif token.dep_ in ("attr", "acomp"):
                    relationship = token.text

            #if subj and obj not found using basic approach , attempt using entity modifiesr
            if not subject or not obj:
                for token in sent:
                    if token.ent_type_ == "PERSON":
                        if not subject:
                            subject = token.text
                        elif not obj:
                            obj = token.text
            # Print the extracted information for each sentence
            if subject and obj:
                # print("Sentence:", sent)
                # print("Subject:", subject)
                # print("Object:", obj)
                # print("Relationship:", relationship)
                # print("--------------------")

                #adding nodes and egdes
                G.add_node(subject)
                G.add_node(obj)
                G.add_edge(subject, obj, relationship = relationship)

# print("test 4")

#drawing the directed graph 
pos = nx.spring_layout(G)
node_labels = {node:node for node in G.nodes()}
edge_labels = {(u,v): data['relationship'] for u,v , data in G.edges(data = True)}

nx.draw(G, pos, with_labels = True, node_size = 2000, font_size = 10, font_color='black', node_color='skyblue', edge_color='gray', arrowsize=12)
nx.draw_networkx_labels(G, pos, labels=node_labels)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')


# Display the graph
plt.title("Entities and Relationships Graph")
plt.show()



