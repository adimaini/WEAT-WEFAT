# WEAT-WEFAT
Replication of WEAT and WEFTA code from Dr. Caliskan's research papers on human-like bias in language corpora that are derived automatically in state-of-the-art machine learning models. The associated research papers are available here:
* [Semantics derived automatically from language corpora contain human-like biases](https://science.sciencemag.org/content/356/6334/183.abstract)
* [Detecting Emergent Intersectional Biases: Contextualized Word Embeddings Contain a Distribution of Human-like Biases](https://arxiv.org/abs/2006.03955)
* [ValNorm: A New Word Embedding Intrinsic Evaluation Method Reveals Valence Bases are Consistent Across Languages and Over Decades ](https://arxiv.org/abs/2006.03950)

## Contents
1. lib/weat.py

This python file contains the Word Embedding Association Test (WETA) and Work Embedding Factual Association Test (WEFTA) implementations. 

2. main.ipynb

This jupyter notebook contains the main file that runs the WETA on 10 datasets that were used to conduct Implicit Association Tests (IAT). 

3. targets_attributes_data/

This folder contains the 10 datasets that each have 2 sets of targets and attributes. 

## Future Implementation
1. The code can be improved to add tests for WEFTA. 
