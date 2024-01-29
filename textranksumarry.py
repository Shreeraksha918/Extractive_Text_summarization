
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
from heapq import nlargest

def summarizer(rawdocs):
    stopwords = set(STOP_WORDS)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)

    # Sentence Tokenization
    sent_tokens = [sent for sent in doc.sents]

    # Create a graph
    G = nx.Graph()

    # Add nodes for each sentence
    G.add_nodes_from(sent_tokens)

    # Compute sentence similarity and add edges
    for i in range(len(sent_tokens)):
        for j in range(i + 1, len(sent_tokens)):
            sim_score = cosine_similarity(
                nlp(sent_tokens[i].text).vector.reshape(1, -1),
                nlp(sent_tokens[j].text).vector.reshape(1, -1)
            )[0][0]
            G.add_edge(sent_tokens[i], sent_tokens[j], weight=sim_score)

    # Apply TextRank algorithm
    scores = nx.pagerank(G)

    # Select top sentences as the summary
    select_len = int(len(sent_tokens) * 0.3)
    summary = nlargest(select_len, scores, key=scores.get)

    # Convert summary to text
    final_summary = [sent.text for sent in summary]
    summary = ' '.join(final_summary)

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))

# Example usage
#text = '''Your input text here.'''
#summary, doc, original_length, summary_length = text_rank_summarizer(text)
#print("Original Length:", original_length)
#print("Summary Length:", summary_length)
#print("Summary:", summary)
