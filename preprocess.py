import spacy
from nltk.corpus import stopwords
import re
import pandas as pd

# Initialize Spacy for lemmatization
nlp = spacy.load('en_core_web_sm')

# NLTK stop words
# nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Delete this from titles
title_negative_list = [
    'entry',
    'junior', 
    'medior', 
    'senior', 
    'i', 
    'I',
    'ii', 
    'iii',
    'iv',
    'hybrid',
    'remote',
    'full',
    'time'
]

# Delete the whole job
job_negative_list = [
    'hr',
    'sustainability',
    'health',
    'medical',
    'clinical',
    'knowledge',
    'athletic',
    'foreign',
    'authority',
    'assistant',
    'administrator',
    'human',
    'staff',
    'program',
    'agent',
    'dean',
    'career',
    'counselor',
    'librarian',
    'library',
    'curator',
    'recruitment',
    'biology',
    'university',
    'educational',
    'educator',
    'teacher',
    'curriculum',
    'academic',
    'education',
    'environmental',
    'planner',
    'support',
    'energy',
    'researcher',
    'research',
    'planner',
    'resource',
    'economist',
    'planning',
    'communication',
    'communicational',
    'hotel',
    'laboratory'
]

replacements = {
    'sr': 'senior',
    'mid': 'medior',
    'jr': 'junior',
    'mgr': 'manager',
    'svp': 'senior vice president',
    'vp': 'vice president',
    'avp': 'assistant vice president',
    'dev': 'developer',
    'pm': 'project manager',
    'ml': 'machine learning',
    'ai': 'artificial intelligence',
    'learn': 'learning',
    'datum': 'data',
    'systems': 'system',
    'it': 'information technology',
    'qa': 'quality assurance'
}


def preprocess_title(text):
    text = text.lower()
    text = text.replace('-', ' ')
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)

    # Filter out entities labeled as organizations or cities (GPE)
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'GPE']]
    filtered_text = [token.text for token in doc if not any(entity in token.text for entity in entities)]

    # Lemmatize the filtered text
    lemmatized = [token.lemma_ for token in nlp(' '.join(filtered_text))]

    # Apply replacements for abbreviations after lemmatization
    replaced_text = [replacements.get(word, word) for word in lemmatized]

    # Additional step to handle compound phrases
    replaced_text = ' '.join(replaced_text).split()

    # Drop rows which title's specified in the negative list
    filtered_text = [word for word in replaced_text if word not in title_negative_list]

    # Filter out negative list words and stop words after replacements
    cleaned_text = [word for word in filtered_text if word not in stop_words]

    return ' '.join(cleaned_text)


def preprocess_description(text):
    # Filter out entities labeled as organizations or cities (GPE)
    doc = nlp(text)
    entities = [ent.text for ent in doc.ents if ent.label_ in ['ORG', 'GPE']]
    filtered_text = [token.text for token in doc if not any(entity in token.text for entity in entities)]

    # Convert filtered text to a string for further processing
    text = ' '.join(filtered_text)

    # Lowercase the text
    text = text.lower()

    # Replace hyphens and remove numbers
    text = text.replace('-', ' ')
    text = re.sub(r'\d+', '', text)

    # Lemmatize the text
    doc = nlp(text)
    lemmatized_tokens = [token.lemma_ for token in doc]

    # Apply replacements for abbreviations
    replaced_text = [replacements.get(word, word) for word in lemmatized_tokens]

    # Filter out stop words
    cleaned_text = [word for word in replaced_text if word not in stop_words]

    # Remove extra white spaces
    final_text = ' '.join(cleaned_text)
    final_text = re.sub(r'\s+', ' ', final_text).strip()

    return final_text


def filter_jobs(df):
    mask = df['title'].apply(lambda x: any(job in x for job in job_negative_list))
    return df[~mask]

# Function to return preprocessed titles
def get_preprocessed_titles(titles):
    return [preprocess_title(title) for title in titles]

# Function to return all words from preprocessed titles
def get_all_words(preprocessed_titles):
    tokenized_titles = [title.split() for title in preprocessed_titles]
    return [word for title in tokenized_titles for word in title]

# Function to return preprocessed descriptions
def get_preprocessed_descriptions(descriptions):
    return [preprocess_description(description) for description in descriptions]

"""
df = pd.read_csv('input/raw_jobs_all.csv')

df['title'] = get_preprocessed_titles(df['title'])
df = filter_jobs(df)
df['description'] = get_preprocessed_descriptions(df['description'])
preprocessed_descriptions = df['description']

df.to_csv('input/preprocessed_jobs_all.csv', index=False)
"""

title = ['Senior ML Specialist at Microsoft', 'Systems Architect II (California)', 'VP of Service Delivery Applications Shared Services',  'Public Health Analyst']
print(get_preprocessed_titles(title))