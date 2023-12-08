import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import jaccard_score
import numpy as np

#/////////////////////////////////////////
#  IMPORT DATASET AND DICTIONARY
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
df = pd.read_csv('preprocessed_jobs_all.csv')
preprocessed_descriptions = df['description']
preprocessed_titles = df['title']

df_esco = pd.read_csv('esco/esco_skill_dictionary.csv')
esco_skills = df_esco['skills']
#esco_skills = get_preprocessed_titles(esco_skills)

#/////////////////////////////////////////
#  JACCARD SIMILARITY 
#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

# Function to calculate Jaccard similarity
def calculate_jaccard_similarity(text1, text2):
    vectorizer = CountVectorizer(binary=True)
    vec = vectorizer.fit_transform([text1, text2]).toarray()
    return jaccard_score(vec[0], vec[1])

# Create an empty matrix with zeros
similarity_matrix = np.zeros((len(preprocessed_descriptions), len(esco_skills)))

# Calculate Jaccard similarities
for i, description in enumerate(preprocessed_descriptions):
    for j, skill in enumerate(esco_skills):
        similarity = calculate_jaccard_similarity(description, skill)
        similarity_matrix[i][j] = similarity

# Convert the matrix to a DataFrame for better readability
similarity_df = pd.DataFrame(similarity_matrix, columns=esco_skills, index=df['title'])

# Export the similarity matrix to an Excel file
similarity_df.to_excel('jaccard_similarity_matrix.xlsx')