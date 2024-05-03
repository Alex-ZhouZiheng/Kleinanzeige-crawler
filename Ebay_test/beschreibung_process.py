import nltk

def process_description(description):
    # Tokenize the description
    tokens = nltk.word_tokenize(description)
    # Lowercase the tokens
    tokens = [token.lower() for token in tokens]
    # Remove stopwords in german

    stopwords = nltk.corpus.stopwords.words('german')
    tokens = [token for token in tokens if token not in stopwords]
    return tokens


