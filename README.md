<h1> Podobni Péter - SZAKDOLGOZAT</h1>
## Alkalmazásintegráció területén szükséges kompetenciák azonosítása szöveganalitikával
## Álláshirdetések elemzése tananyagfejlesztés megalapozására

### 4.4 Adatgyűjtés és adattisztítás
  [Scraper script](site_indeed.py) \
  [Nyers adatkészlet excel](input/indeed_merged.csv)

### 4.5 Adatok előkészítése az elemzésre
  [Szöveg előkészítő script](preprocess.py) \
  [Előkészített adatkészlet excel](input/preprocessed_jobs_all.csv) 

### 4.6 Munkakörök címeinek elemzése szöveganalitikai eszközökkel
#### 4.6.1 Munkakör címek szavainak gyakoriságvizsgálata
  [N-gram gyakoriságok script](title/title_freq_ngrams_all.ipynb) \
  [N-gram gyakoriságok tapasztalati szintekre bontva script](title/title_freq_ngrams_levels.ipynb)
  
#### 4.6.2 Munkakörök csoportokra osztása
  [Klasztereket létrehozó script](title/title_cluster.ipynb) \
  [Klaszterek txt](title/clusters.txt) 
  
### 4.7 Kompetenciák feltérképezése az álláshirdetésekben

#### 4.7.1 Álláshirdetések szavainak gyakoriságelemzése

#### 4.7.2 Szótáralapú gyakoriságviszgálat saját szótárral

#### 4.7.3 Szótárépítés ESCO osztályozással további hasonlóságvizsgálathoz

### 4.7.4 Jaccard hasonlósági mátrix építése az ESCO szótárra

### 4.7.5 Koszinusz hasonlósági mátrix építése GloVe modellel az ESCO szótárra

### 4.7.6 Koszinusz hasonlósági mátrix építése S-BERT modellel az ESCO szótárra
