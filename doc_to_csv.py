import csv
import re
from docx import Document

def clean_skill_text(text):
    cleaned_text = re.sub(r'\[.*?\]', '', text)  
    cleaned_text = ' '.join(cleaned_text.split())  # 
    return cleaned_text.strip()  

def contains_hyperlinks(paragraph):
    return any(link is not None for link in paragraph.hyperlinks)

document = Document('esco/skills_raw.docx') 

hyperlink_texts = []

for paragraph in document.paragraphs:
    if "Essential Skills and Competences" in paragraph.text:
        cleaned_text = clean_skill_text(paragraph.text)
        if cleaned_text:
            hyperlink_texts.append(cleaned_text)

    if contains_hyperlinks(paragraph):
        for link in paragraph.hyperlinks:
            cleaned_text = clean_skill_text(link.text)
            if cleaned_text:
                hyperlink_texts.append(cleaned_text)

csv_file_path = 'esco_skill_dictionary.csv'

with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['skills'])

    for text in hyperlink_texts:
        csv_writer.writerow([text])
