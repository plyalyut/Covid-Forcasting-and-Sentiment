from flair.data import Sentence
from flair.models import TextClassifier
import numpy as np

class SentimentAnalysis:

    def __init__(self):
        """
        Sets up the sentiment analysis framework.
        """

        self.classifer = TextClassifier.load('en-sentiment')

    def calculate_overall_sentiment(self, sentences):
        flair_sents = self.__load_sentences(sentences)
        positives, negatives = self.__predict_sentiment(flair_sents)
        return positives, negatives

    def __load_sentences(self, sentences):
        """
        Takes in a list of sentences and does sentiment analysis on it.
        :param sentences: List[String]
        :return: Flair
        """
        return [Sentence(s) for s in sentences]

    def __predict_sentiment(self, sentence_list):
        """
        Predicts the sentiment from the sentences provided
        :param sentence_list: List[Sentence]
        :return:
        """
        positives = 0
        negatives = 0

        for sent in sentence_list:
            self.classifer.predict(sent)
            if sent.labels[0].value == "NEGATIVE":
                negatives += 1
            else:
                positives += 1

        return positives, negatives
