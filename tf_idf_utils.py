import operator
import scipy
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


def dict2list_of_all_occurrences(a_dict):
    return [label
            for label, freq in a_dict.items()
            for _ in range(freq)]


assert dict2list_of_all_occurrences(a_dict={'a': 3, 'b': 1}) == ['a', 'a', 'a', 'b']


def compute_tfidf(corpus_name2corpus,
                  min_corpus_freq=1,
                  verbose=0):
    """
    compute tf idf values

    :param min_corpus_freq:
    :param verbose:
    :param dict corpus_name2corpus: e.g.,
    {
      'text1' : 'A rose rose rose rose',
      'text2' : 'A rose is a flower',
      'text3' : 'A book is nice'
    }
    """
    all_corpus_names = list(corpus_name2corpus.keys())
    index2corpus_name = {
        index: corpus_name
        for index, corpus_name in enumerate(all_corpus_names)
    }

    corpus2label2tf_idf_value = {
        corpus_name: {}
        for corpus_name in all_corpus_names
    }

    # you can adapt min_df to restrict the representation to more frequent words e.g. 2, 3, etc..
    vectorizer = CountVectorizer(min_df=min_corpus_freq,  # in how many documents the term minimally occurs
                                 tokenizer=lambda x: x.split(' '))  # we split on space
    corpus_counts = vectorizer.fit_transform([corpus_name2corpus[corpus_name]
                                              for corpus_name in all_corpus_names])
    tfidf_transformer = TfidfTransformer()
    sents_tfidf = tfidf_transformer.fit_transform(corpus_counts)

    if verbose >= 1:
        num_corpora, vocab_size = sents_tfidf.shape
        print()
        print(f'minimum corpus freq: {min_corpus_freq}')
        print(f'number of corpora: {num_corpora}')
        print(f'vocabulary size: {vocab_size}')

    vocab = vectorizer.get_feature_names()
    index2vocab_member = {
        index: vocab_member
        for index, vocab_member in enumerate(vocab)
    }
    cx = scipy.sparse.coo_matrix(sents_tfidf)
    for corpus_index, vocab_member_index, tfidf_value in zip(cx.row, cx.col, cx.data):
        corpus_name = index2corpus_name[corpus_index]
        vocab_member = index2vocab_member[vocab_member_index]
        corpus2label2tf_idf_value[corpus_name][vocab_member] = tfidf_value

    if verbose >= 2:
        for corpus, label2tf_idf_value in corpus2label2tf_idf_value.items():
            print()
            print(corpus)
            counter = 0
            for label, tf_idf_value in sorted(label2tf_idf_value.items(),
                                              key=operator.itemgetter(1),
                                              reverse=True):
                print(label, round(tf_idf_value, 2))
                counter += 1
                if counter == 5:
                    break


    return corpus2label2tf_idf_value
