# -*- coding: utf-8 -*-

import datetime, json, operator, pprint, unittest
from types import NoneType

# import nlp_app_settings as app_settings
# import django, pattern
import pattern
from pattern import vector
# from pattern.vector import Document, Corpus


class CorpusWrapper( object ):
  '''
  '''

  def __init__(self):
    self.time_start = datetime.datetime.now()
    self.original_texts = []
    self.doc_max_keywords = 20
    self.docs = []
    self.doc_keywords = {}
    self.doc_corpus_keywords = {}
    self.corpus = None

  def load_texts( self, texts ):
    assert type(texts) == list
    for text_dict in texts:
      assert type(text_dict) == dict
      assert sorted(text_dict.keys()) == [u'name', u'ustring']
      self.original_texts.append( text_dict )
      d = vector.Document( text_dict[u'ustring'], name=text_dict[u'name'], stemmer=vector.PORTER, threshold=1 )
      self.docs.append( d )

  def generate_doc_keywords(self):
    for doc in self.docs:
      full_vector = doc.vector
      sorted_full_vector = self.sort_full_vector( full_vector )
      self.doc_keywords[doc.name] = sorted_full_vector[0:self.doc_max_keywords]
    # print u'- doc_keywords:'; pprint.pprint( self.doc_keywords )

  def sort_full_vector(self, full_vector):
    assert type( json.loads( json.dumps(full_vector) ) ) == dict  # full_vector is of type pattern.vector.Vector, but looks like a dict
    sorted_full_vector = sorted( full_vector.iteritems(), key=operator.itemgetter(1), reverse=True )  # makes list of tuples
    assert type(sorted_full_vector) == list; assert type(sorted_full_vector[0]) == tuple
    return sorted_full_vector

  def make_corpus(self):
    self.corpus = vector.Corpus( documents=[] )
    for doc in self.docs:
      self.corpus.append( doc )

  def generate_doc_corpus_keywords(self):
    for doc in self.corpus.documents:
      full_vector = doc.vector
      sorted_full_vector = self.sort_full_vector( full_vector )
      self.doc_corpus_keywords[doc.name] = sorted_full_vector[0:self.doc_max_keywords]
    # print u'- doc_corpus_keywords'; pprint.pprint( self.doc_corpus_keywords )





# ##
# ## tests
# ##


class CorpusWrapperTest( unittest.TestCase ):

  def test_load_texts(self):
    cw = CorpusWrapper()
    self.assertEqual( cw.original_texts, [] )
    doc_egypt_reuters = open( u'./nlp_app/documents/egypt_reuters.txt' ).read().decode(u'utf-8', u'replace')
    doc_egypt_washpost = open( u'./nlp_app/documents/egypt_washington_post.txt' ).read().decode(u'utf-8', u'replace')
    doc_apple_buswk = open( u'./nlp_app/documents/apple_business_week.txt' ).read().decode(u'utf-8', u'replace')
    doc_samsung_ars = open( u'./nlp_app/documents/samsung_ars.txt' ).read().decode(u'utf-8', u'replace')
    cw.load_texts( [
        { u'name': u'doc_egypt_reuters', u'ustring': doc_egypt_reuters },
        { u'name': u'doc_egypt_washpost', u'ustring': doc_egypt_washpost },
        { u'name': u'doc_apple_buswk', u'ustring': doc_apple_buswk },
        { u'name': u'doc_samsung_ars', u'ustring': doc_samsung_ars },
        ] )
    self.assertEqual( len(cw.original_texts), 4 )

  def test_generate_doc_keywords(self):
    cw = CorpusWrapper()
    doc_egypt_reuters = open( u'./nlp_app/documents/egypt_reuters.txt' ).read().decode(u'utf-8', u'replace')
    doc_egypt_washpost = open( u'./nlp_app/documents/egypt_washington_post.txt' ).read().decode(u'utf-8', u'replace')
    doc_apple_buswk = open( u'./nlp_app/documents/apple_business_week.txt' ).read().decode(u'utf-8', u'replace')
    doc_samsung_ars = open( u'./nlp_app/documents/samsung_ars.txt' ).read().decode(u'utf-8', u'replace')
    cw.load_texts( [
        { u'name': u'doc_egypt_reuters', u'ustring': doc_egypt_reuters },
        { u'name': u'doc_egypt_washpost', u'ustring': doc_egypt_washpost },
        { u'name': u'doc_apple_buswk', u'ustring': doc_apple_buswk },
        { u'name': u'doc_samsung_ars', u'ustring': doc_samsung_ars },
        ] )
    doc = cw.original_texts[0]
    self.assertEqual( type(doc), dict )
    cw.generate_doc_keywords()
    self.assertEqual( sorted(cw.doc_keywords.keys()), [u'doc_apple_buswk', u'doc_egypt_reuters', u'doc_egypt_washpost', u'doc_samsung_ars'] )

  def test_make_corpus(self):
    cw = CorpusWrapper()
    doc_egypt_reuters = open( u'./nlp_app/documents/egypt_reuters.txt' ).read().decode(u'utf-8', u'replace')
    doc_egypt_washpost = open( u'./nlp_app/documents/egypt_washington_post.txt' ).read().decode(u'utf-8', u'replace')
    doc_apple_buswk = open( u'./nlp_app/documents/apple_business_week.txt' ).read().decode(u'utf-8', u'replace')
    doc_samsung_ars = open( u'./nlp_app/documents/samsung_ars.txt' ).read().decode(u'utf-8', u'replace')
    cw.load_texts( [
        { u'name': u'doc_egypt_reuters', u'ustring': doc_egypt_reuters },
        { u'name': u'doc_egypt_washpost', u'ustring': doc_egypt_washpost },
        { u'name': u'doc_apple_buswk', u'ustring': doc_apple_buswk },
        { u'name': u'doc_samsung_ars', u'ustring': doc_samsung_ars },
        ] )
    self.assertEqual( type(cw.corpus), NoneType )
    cw.make_corpus()
    self.assertEqual( type(cw.corpus), pattern.vector.Corpus )

  def test_generate_doc_corpus_keywords(self):
    cw = CorpusWrapper()
    doc_egypt_reuters = open( u'./nlp_app/documents/egypt_reuters.txt' ).read().decode(u'utf-8', u'replace')
    doc_egypt_washpost = open( u'./nlp_app/documents/egypt_washington_post.txt' ).read().decode(u'utf-8', u'replace')
    doc_apple_buswk = open( u'./nlp_app/documents/apple_business_week.txt' ).read().decode(u'utf-8', u'replace')
    doc_samsung_ars = open( u'./nlp_app/documents/samsung_ars.txt' ).read().decode(u'utf-8', u'replace')
    cw.load_texts( [
        { u'name': u'doc_egypt_reuters', u'ustring': doc_egypt_reuters },
        { u'name': u'doc_egypt_washpost', u'ustring': doc_egypt_washpost },
        { u'name': u'doc_apple_buswk', u'ustring': doc_apple_buswk },
        { u'name': u'doc_samsung_ars', u'ustring': doc_samsung_ars },
        ] )
    cw.make_corpus()
    cw.generate_doc_corpus_keywords()
    self.assertEqual( sorted(cw.doc_corpus_keywords.keys()), [u'doc_apple_buswk', u'doc_egypt_reuters', u'doc_egypt_washpost', u'doc_samsung_ars'] )





if __name__ == "__main__":
  unittest.main()
