#!/usr/bin/python
# -*- coding: utf-8 -*-
# DATE: 2023/03/02
# Author: Irfan TOOR
# file : pipeline.py

from abc import ABC
import pandas as pd
import spacy
import string
import re
from nltk.stem import SnowballStemmer, WordNetLemmatizer

class Pipeline(ABC):
    # stopwords
    _add_to_stopwords = []
    _remove_from_stopwords = []

    # pos tags
    _excluded_tags = []

    # natural language processing
    _use_nlp = False

    # stemming or lemmatization
    _use_stemming = False
    _use_lemmatization = True

    # internal processing
    _pipeline_built = False

    def __init__(self,
        add_to_stopwords:list=[],
        remove_from_stopwords:list=[],
        excluded_tags:list=[],
        use_nlp:bool=False,
        use_stemming:bool=False,
        use_lemmatization:bool=True
        ) -> None:
        return
        super().__init__()

        self.add_to_stopwords(add_to_stopwords)
        self.remove_from_stopwords(remove_from_stopwords)
        self.excluded_tags(excluded_tags)

        self.use_nlp(use_nlp)
        self.use_stemming(use_stemming)
        self.use_lemmatization(use_lemmatization)

        try:
            self._nlp = spacy.load('en_core_web_sm')
        except:
            raise Exception("en_core_web_sm missing : python -m spacy download en_core_web_sm")

    def add_to_stopwords(self, add_to_stopwords:list):
        """Add additional words to be considered as stopwords"""
        self._add_to_stopwords = add_to_stopwords

    def remove_from_stopwords(self, remove_from_stopwords:list):
        """Remove the words that will not be considered as stopwords"""
        self._remove_from_stopwords = remove_from_stopwords

    def excluded_tags(self, excluded_tags:list):
        """POS tags to be removed, while processing the text"""
        self._excluded_tags = excluded_tags

    def use_nlp(self, use_nlp:bool):
        """
        Use nlp - True : va utiliser spacy.nlp pour faire les jetons
        c'est lent, mais precis, utiliser False pour un processing rapid
        """
        self._use_nlp = use_nlp

    def use_stemming(self, use_stemming:bool):
        """Use stemming technique"""
        self._use_stemming = use_stemming

    def use_lemmatization(self, use_lemmatization:bool):
        """Use lemmatization technique"""
        self._use_lemmatization = use_lemmatization

    def reset(self):
        """Reset the pipeline, so that it can be rebuild with newer parameters"""
        self._pipeline_built = False

    def build(self):
        """Builds the pipeline, essentially compiling or loading the required components"""
        if self._pipeline_built:
            return

        # todo -- add self._pipline_building to avoid DOS attack
        self._pipeline_built = True

        # ~326 stopwords (en_core_web_sm)
        self._stopwords = self._nlp.Defaults.stop_words.copy()

        # add requested
        for word in self._add_to_stopwords:
            self._stopwords |= {word}

        # remove requested
        self._stopwords = [word for word in self._stopwords if word not in self._remove_from_stopwords]

        # @ va etre utiliser pour marquer les @USER et/ou @URL etc.
        self._tr_table = ''.maketrans('', '', string.punctuation.replace('@', ''))

        # regex for cleaning
        self._re_whitespace = re.compile(r"\s+")
        self._re_dot = re.compile(r"\.+")
        self._re_user = re.compile(r"(?i)@[a-z0-9_]+")
        self._re_tag = re.compile(r"(?:\#\S*)")
        self._re_url = re.compile(r"((http|ftp|https):\/\/[\w\-]+(\.[\w\-]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?)" )
        self._re_number = re.compile(r"\d+")
        self._re_special = re.compile(r"\&\w+\;")

        # Stemming
        if (self._use_stemming):
            self._stemmer = SnowballStemmer('english')

        # lemmatization
        if (self._use_lemmatization):
            self._lemmatizer = WordNetLemmatizer()

    def _toupper(self, match):
        """Converts the matched expression to uppercase"""
        if match.group() is not None:
            return match.group().upper()

    def _process_text(self, text:str):
        """process a single line of text, passing it through the pipeline"""
        # espace suplémentaires => ' '
        text = self._re_whitespace.sub(' ', text)

        # &quote;, &...;, etc. => ''
        text = self._re_special.sub('', text)

        # @any_username => @USER
        text = self._re_user.sub('@USER', text)

        # http://... ftp://.., https://... => @URL
        text = self._re_url.sub('@URL', text)

        # . ... => ''
        text = self._re_dot.sub(' ', text)

        # #hashtags => HASHTAG (les mots en majuscule)  ex: #fire => FIRE
        text = self._re_tag.sub(self._toupper, text)

        # 1 123 98765 42 => ''
        text = self._re_number.sub('', text)

        # tokeniz -- 'Hello Wolrd' => ['Hello', 'World']
        if self._use_nlp: # slow
            tokens = [x.orth_ for x in self._nlp(text)]
        else: # fast ;-)
            # he'll => he 'll etc.
            text = text.replace("'", " '")
            tokens = text.strip(' ').split(' ')

        # minuscule
        tokens = [x.lower() if x!=x.upper() else x for x in tokens]

        # stopwords => ''
        tokens = [x for x in tokens if x not in self._stopwords]

        # punctuations => ''
        tokens = [word.translate(self._tr_table) for word in tokens]

        # '' => supprimer
        tokens = [x for x in tokens if x != '']

        # petite jetons => supprimmer
        tokens = [x for x in tokens if len(x) > 1]

        # lemmatization
        if (self._use_lemmatization):
            tokens = [self._lemmatizer.lemmatize(word,'v') for word in tokens]

        # stemming
        if (self._use_stemming):
            tokens = [self._stemmer.stem(word) for word in tokens]

        return tokens

    def process(self, phrases:list):
        """process the given list of sentences"""
        if (not self._pipeline_built):
            self.build()

        return [self._process_text(phrase) for phrase in phrases]
