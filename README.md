# Cross Document Coreference Resolution

NLP Course project on resolving entities and coreference chains across multiple documents

##Authors
Girish K, Vijaya S

##Goal: 
The goal of this project is to resolve entities and relations across multiple documents. This file describes the folders under this project, including the attempted technqiues


##Dependencies:
A bulk of the code needs to following python libraries:
* Numpy
* Scipy
* Sklearn
* Theano
* Newspaper
* Simplejson
* Gensim
* Stanford CoreNLP (2015-12-09)
* GloVE
* Google word2vec
* Skip-thought vectors (sent2vec)


##Big Files
Some of our data is too huge to push to Github, so we provide links to download this data. We list these files below : 

1. SNLI Corpus  : http://nlp.stanford.edu/projects/snli/
2. Stanford CoreNLP : http://stanfordnlp.github.io/CoreNLP/download.html
3. Skip-thought vectors : https://github.com/ryankiros/skip-thoughts
4. GloVe: http://nlp.stanford.edu/projects/glove/
5. 


##Folders:

###crawlers
This folder contains the crawlers that we used to query the NYTimes API to get article links for the past 20 years, and also the code to scrape the text of these articles, and clean them.  We have excluded the NYTimes dataset we scraped from the repository, and it will be have to be download separately.


###LDA
* The LDA folder contains the toy dataset, and the code that uses Gensim to perform Latent Dirichlet Allocation to identify soft clusters of article, in the file compareSimilarity.py
* The file preprocesses the toy dataset using vocabulary construction, stop word removal, stemming, tf-idf normalization, and outputs the clusters of doucments. 
* The folder also contains the CoreNLP annotations for the following tasks - NER, POS, Lemmatization Dependency parse (Basic and Collapsed), Coreference Chains and OpenIE relations . 


###relation_extraction_from_clusters
*This folder contains our experiments with OpenIE relations, and visualizing a graph using it.

###relation_normalization


###relation_coref_combine
In this folder, we combine relations and coreferences across multiple documents. The result was extremely noisy.



###dependency_parsing
In this folder, we extracted basic dependencies(tree form), and collapsed dependecies(graph form) from the CoreNLP output, and built a visualization interface that can be configured to filter based on head words, sentence_ids, documents, etc. This can be used to visualize similar sentence structures across doucments

###NLI
This folder contains the files with respect to Natural Logic Inference. We experimented with three methods of training a clasifier on this dataset:

* We first use skip-thought vectors to generate 9600 dimension vectors for each sentnce pair in our training fold(are there so many planets in the Milky way? : We used two types of classifers (SVM and Neural Network) to train using these sentence vectors and their gold labels.

* We also tried using lexicalised features as suggested in the original SNLI paper. However, this feature was too sparse, and performed worse than skip-thought vectors, after which we discarded it.

* We also try 600-dimension vectors by concatenating the sum of word vectors for the two sentences in each pair, and used an SVM to train on these vectors.


###TODO
* Remove failed experiments!
* Merge visualization with backend]
* Train under more scalable conditions
* Train using LSTM (as it was proved to give the best results till date)




