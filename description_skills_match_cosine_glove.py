import numpy as np
import pandas as pd
from nltk.util import ngrams
from nltk import word_tokenize
import math


def squared_sum(v):
    """ Compute the squared sum of a vector """
    return math.sqrt(sum([x**2 for x in v]))


def cos_similarity(x, y):
    """ Return cosine similarity between two lists """
    numerator = sum(a*b for a, b in zip(x, y))
    denominator = squared_sum(x) * squared_sum(y)
    return round(numerator / float(denominator), 3) if denominator != 0 else 0


def load_glove_embeddings(glove_file):
    embeddings_dict = {}
    with open(glove_file, 'r', encoding='utf-8') as file:
        for line in file:
            values = line.split()
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
    return embeddings_dict


def encode_sentence_glove(sentence, embeddings_dict, embed_dim=100):
    tokens = sentence.lower().split()
    vectors = [embeddings_dict.get(word, np.zeros((embed_dim,))) for word in tokens]
    if all(np.all(v == 0) for v in vectors):
        return np.zeros((embed_dim,))
    return np.mean(vectors, axis=0)


def generate_ngrams(text, n):
    tokens = word_tokenize(text)
    # Handle cases where there are fewer tokens than 'n'
    if len(tokens) < n:
        return []
    return [' '.join(gram) for gram in ngrams(tokens, n)]


def create_similarity_matrix(job_descriptions, skills, n):
    # Generate n-grams
    job_desc_ngrams = [' '.join(generate_ngrams(desc, n)) for desc in job_descriptions]
    skills_ngrams = [' '.join(generate_ngrams(skill, n)) for skill in skills]

    # Compute embeddings
    job_desc_embeddings = [encode_sentence_glove(desc, glove_embeddings) for desc in job_desc_ngrams]
    skills_embeddings = [encode_sentence_glove(skill, glove_embeddings) for skill in skills_ngrams]

    # Calculate similarity scores
    similarity_matrix = [[cos_similarity(desc_emb, skill_emb) for skill_emb in skills_embeddings] for desc_emb in job_desc_embeddings]

    return pd.DataFrame(similarity_matrix, index=job_descriptions, columns=skills)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#  LOAD DATA
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
glove_embeddings = load_glove_embeddings("glove/glove.6B.100d.txt")

df = pd.read_csv('preprocessed_jobs_all.csv')
prep_descriptions = df['description']

df_esco = pd.read_csv('esco/prep_esco_skill_dictionary.csv')
esco_skills = df_esco['skills']

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#  MATRIX
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
with pd.ExcelWriter('similarity_scores.xlsx') as writer:
    for n in [2]:
        matrix = create_similarity_matrix(prep_descriptions, esco_skills, n)
        matrix.to_excel(writer, sheet_name=f'{n}-grams')

print("Similarity matrix saved to Excel.")
