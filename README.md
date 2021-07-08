# BAGUETTE 🥖: Best analysis of Article Given in a UnifiEd approach Through Time Evolution

### Auteurs

* Yanis Labrak
* Mathias Quillot

### Générer les Stopwords

```bash
cd stopswords
python merge.py
```

### Extraction des concepts les plus importants

Un seul PDF:

```console
python main.py --path=test.pdf
```

En utilisant l'algorithme TF-IDF:

```console
python main.py --path=./ --tf-idf
```

Vous verrez ensuite la liste des mots les plus importants s'afficher à l'écran.

### Dépendences

__Python__:

```bash
pip install -r requirements.txt
```

* Python 2.7+ [Télécharger](https://www.python.org/download/releases/2.7/)
