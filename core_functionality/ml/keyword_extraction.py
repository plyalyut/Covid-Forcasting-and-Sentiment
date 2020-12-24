import spacy
import pytextrank

class KeywordExtractor:
    def __init__(self):
        """
        Loads in the keyword extractor and adds it to the Spacy pipeline.
        """
        self.nlp = spacy.load('en_core_web_sm')
        self.textrank = pytextrank.TextRank()
        self.nlp.add_pipe(self.textrank.PipelineComponent, name='textrank', last=True)

    def extract_keywords(self, sentences):
        """
        Extracts keyphrases from sentences.
        :param sentences: Sentences, List[String]
        :return: List[String] of top 5 keyphrases
        """
        new_sent = " ".join(sentences)
        annotated = self.nlp(new_sent)
        return [phrase.text for phrase in annotated._.phrases[:5]]