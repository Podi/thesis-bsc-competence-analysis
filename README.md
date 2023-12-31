# Podobni Péter - SZAKDOLGOZAT
# Alkalmazásintegráció területén szükséges kompetenciák azonosítása szöveganalitikával
## Álláshirdetések elemzése tananyagfejlesztés megalapozására </h2>

## 4.4 Adatgyűjtés és adattisztítás
  [Web scraper script](site_indeed.py) \
  [Nyers adatkészlet csv](input/indeed_merged.csv)

## 4.5 Adatok előkészítése az elemzésre
  [Szöveges adatokat előkészítő script](preprocess.py) \
  [Előkészített adatkészlet csv](input/preprocessed_jobs_all.csv) 

## 4.6 Munkakörök címeinek elemzése szöveganalitikai eszközökkel
### 4.6.1 Munkakör címek szavainak gyakoriságvizsgálata
  [Címek N-gram gyakorisága script](title/title_freq_ngrams_all.ipynb) \
  [Címek N-gram gyakorisága tapasztalati szintekre bontva script](title/title_freq_ngrams_levels.ipynb)
  
### 4.6.2 Munkakörök csoportokra osztása
  [Klasztereket létrehozó script](title/title_cluster.ipynb) \
  [Klaszterek txt](title/clusters.txt) 
  
## 4.7 Kompetenciák feltérképezése az álláshirdetésekben
### 4.7.1 Álláshirdetések szavainak gyakoriságelemzése
  [Leírások N-gram gyakorisága script](description/description_freq_ngrams_all.ipynb) \
  [Leírások N-gram gyakoriságok excel](description/description_freq_ngrams_all.xlsx) 

  [Leírások N-gram gyakorisága & TF-IDF tapasztalati szintekre bontva script](description/description_freq_ngrams_all_tf-idf.ipynb) \
  Top 50 N-gram gyakoriság & TF-IDF: \
    [Junior excel](description/level_comparison/junior_description_top_50_ngrams_tfidf_freq.xlsx) \
    [Medior excel](description/level_comparison/medior_description_top_50_ngrams_tfidf_freq.xlsx) \
    [Senior excel](description/level_comparison/senior_description_top_50_ngrams_tfidf_freq.xlsx) 
  
### 4.7.2 Szótáralapú gyakoriságviszgálat saját szótárral
  [Szótári szavak gyakorisága script](description/dictionary/description_dictionary_freq_tf-idf.ipynb) \
  [Programnyelvek szótára json](description/dictionary/coding_keywords.json) \
  [Szoftverek szótára json](description/dictionary/softwares_keywords.json)

### 4.7.3 Szótárépítés ESCO osztályozással további hasonlóságvizsgálathoz
  [ESCO kompetenciák nyers docx](esco/skills_raw.docx) \
  [ESCO dokumentum feldolgozó script](esco/doc_to_csv.py) \
  [ESCO kompetencia szótár csv](esco/prep_esco_skill_dictionary.csv)

### 4.7.4 Jaccard hasonlósági mátrix építése az ESCO szótárra
  [CountVec & Jaccard hasonlósági mátrix script](description/description_skills_match_jaccard_countvec.py) \
  [Mátrix1 excel](description/matrix/01_similarity_matrix_jaccard_countvec.xlsx)

  [TF-IDF & Jaccard hasonlósági mátrix script](description/description_skills_match_jaccard_tfidf.ipynb) \
  [Mátrix2 excel](description/matrix/02_similarity_matrix_jaccard_tfidf.xlsx)

### 4.7.5 Koszinusz hasonlósági mátrix építése GloVe modellel az ESCO szótárra
  [GloVe & koszinusz hasonlósági mátrix script](description/description_skills_match_cosine_glove.py) \
  [Mátrix3 excel](description/matrix/03_similarity_matrix_cosine_glove.xlsx)
  
### 4.7.6 Koszinusz hasonlósági mátrix építése S-BERT modellel az ESCO szótárra
  [GloVe & koszinusz hasonlósági mátrix script](description/description_skills_match_cosine_sbert.ipynb) \
  [Mátrix4 excel](description/matrix/04_similarity_matrix_cosine_sbert.xlsx)
