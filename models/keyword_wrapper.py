# -*- coding: utf-8 -*-

import datetime, hashlib, json, pprint, unittest
from types import NoneType

import nlp_app_settings as app_settings
import django, pattern
from pattern.vector import Document, PORTER, stem


class KeywordWrapper( object ):
  '''
  Non-django model; wrapper around pattern.vector keyword functions.
  See views.keywords() for usage.
  '''

  def __init__(self):
    self.time_start = None
    self.params = {}
    self.original_text = None
    self.original_text_md5_hash = None
    self.document_raw = None
    self.document_raw_count = None
    self.document_thresh_stemmed = None
    self.document_thresh_unstemmed = None
    self.top_num = 10
    self.keywords_stemmed = None
    self.keywords_unstemmed = None
    self.keywords_unstemmed_additional = None
    self.keywords_stemmed_simple = []
    self.explore_json_string = None
    self.simple_json_string = None

  def get_params( self, dj_request ):
    assert type(dj_request) == django.core.handlers.wsgi.WSGIRequest
    if dj_request.method == u'GET':
      for item in dj_request.GET.items():
        key = item[0]; value = item[1]
        self.params[key] = value
    else:  # POST
      for item in dj_request.POST.items():
        key = item[0]; value = item[1]
        self.params[key] = value

  def load_text( self, text ):
    self.time_start = datetime.datetime.now()
    self.document_raw = Document( text, threshold=0 )
    self.document_raw_count = self.document_raw.count
    self.document_thresh_stemmed = Document( text, stemmer=PORTER, threshold=1 )
    self.document_thresh_unstemmed = Document( text, threshold=1 )
    self.original_text = text
    self.original_text_md5_hash = hashlib.md5(self.original_text.encode(u'utf-8', u'replace')).hexdigest().decode(u'utf-8', u'replace')  # takes source-u-string, makes source-string, gets hash-string, makes hash-u-string

  def set_top_num( self ):
    assert type(self.document_raw) == pattern.vector.Document
    for i in range( 1, self.document_raw.count, 1000 ):
      self.top_num += 1
      if self.top_num == 50:
        break

  def make_keywords_stemmed_simple( self ):
    assert type(self.document_thresh_stemmed) == pattern.vector.Document
    self.keywords_stemmed = self.document_thresh_stemmed.keywords( top=self.top_num )
    for kw_tuple in self.keywords_stemmed:
      score = kw_tuple[0]; word = kw_tuple[1]
      self.keywords_stemmed_simple.append( word )

  def make_default_keywords( self ):
    '''keywords stemmed & unstemmed'''
    assert type(self.document_thresh_stemmed) == pattern.vector.Document
    assert type(self.document_thresh_unstemmed) == pattern.vector.Document
    self.keywords_stemmed = self.document_thresh_stemmed.keywords( top=self.top_num )
    self.keywords_unstemmed = self.document_thresh_unstemmed.keywords( top=self.top_num )
    
  def make_additional_keywords( self ):
    '''unstemmed words not in stemmed list'''
    assert type(self.keywords_stemmed) == list
    if len( self.keywords_stemmed ) > 0:
      assert type(self.keywords_stemmed[0]) == tuple
    assert type(self.keywords_unstemmed) == list
    if len( self.keywords_unstemmed ) > 0:
      assert type(self.keywords_unstemmed[0]) == tuple
    ## make simple stemmed keyword list from (score, word) tuple
    temp_simple_stemmed = []
    for kw_tuple in self.keywords_stemmed:
      score = kw_tuple[0]; word = kw_tuple[1]
      temp_simple_stemmed.append( word )
    ## add any additional unstemmed keywords (whose stems aren't in temp_simple_stemmed )
    self.keywords_unstemmed_additional = []
    for kw_tuple in self.keywords_unstemmed:
      score = kw_tuple[0]; word = kw_tuple[1]
      if word not in temp_simple_stemmed:  # TODO: time using sets here instead
        if stem( word, stemmer=PORTER ) not in temp_simple_stemmed:
          self.keywords_unstemmed_additional.append( kw_tuple )

  def build_explore_json_string( self ):
    import hashlib
    d = {
      u'count_words_raw': len( self.original_text.split() ),
      u'count_words_analyzed': self.document_raw.count,
      u'count_words_repeating_stemmed': self.document_thresh_stemmed.count,
      u'count_words_repeating_unstemmed': self.document_thresh_unstemmed.count,
      u'count_keywords_stemmed': len( self.keywords_stemmed ),
      u'count_keywords_unstemmed': len( self.keywords_unstemmed ),
      u'count_keywords_unstemmed_additional': len( self.keywords_unstemmed_additional ),
      u'hash_md5': self.original_text_md5_hash,
      u'keywords_stemmed': self.keywords_stemmed,
      u'keywords_unstemmed': self.keywords_unstemmed,
      u'keywords_unstemmed_additional': self.keywords_unstemmed_additional,
      u'repeating_words_unstemmed': self.document_thresh_unstemmed.terms,
      u'time_start': unicode( self.time_start ),
      u'time_taken': unicode( datetime.datetime.now() - self.time_start ),
      u'docs': app_settings.DOCS_URL
      }
    self.explore_json_string = json.dumps( d, sort_keys=True, indent=2 )

  def build_simple_json_string( self ):
    d = {
      u'count_keywords_stemmed': len( self.keywords_stemmed ),
      u'keywords_stemmed': self.keywords_stemmed_simple,
      u'hash_md5': self.original_text_md5_hash,
      u'time_start': unicode( self.time_start ),
      u'time_taken': unicode( datetime.datetime.now() - self.time_start ),
      u'docs': app_settings.DOCS_URL
      }
    self.simple_json_string = json.dumps( d, sort_keys=True, indent=2 )


##
## tests
##


class KeywordWrapperTest( unittest.TestCase ):

  _sample_text = u'''
    Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal.
    Now we are engaged in a great civil war, testing whether that nation, or any nation, so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.
    But, in a larger sense, we can not dedicate, we can not consecrate, we can not hallow this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us—that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion—that we here highly resolve that these dead shall not have died in vain—that this nation, under God, shall have a new birth of freedom—and that government of the people, by the people, for the people, shall not perish from the earth.
    '''

  def test_load_test(self):
    '''loads text & makes default document-objects: # raw, thresh-stemmed, thresh-unstemmed'''
    kw = KeywordWrapper()
    self.assertEqual( type(kw.document_raw), NoneType )
    self.assertEqual( type(kw.original_text_md5_hash), NoneType )
    kw.load_text( self._sample_text )
    self.assertEqual( type(kw.document_raw), pattern.vector.Document )
    self.assertEqual( kw.document_raw_count, 84 )
    self.assertEqual( kw.original_text_md5_hash, u'314b82e369aa6f1e521fe40c5ef53360' )

  def test_set_top_num(self):
    '''starts at 10; increases +1 every thousand words up to 50'''
    kw = KeywordWrapper()
    self.assertEqual( kw.top_num, 10 )
    kw.load_text( u'word ' * 10000 )
    kw.set_top_num()
    self.assertEqual( kw.document_raw.count, 10000 )
    self.assertEqual( kw.top_num, 20 )

  def test_make_keywords_stemmed_simple(self):
    kw = KeywordWrapper()
    kw.load_text( self._sample_text )
    kw.set_top_num()
    kw.make_keywords_stemmed_simple()
    self.assertEqual( kw.keywords_stemmed_simple, [u'dedic', u'nation', u'live', u'dead', u'peopl', u'conceiv', u'consecr', u'war'] )

  def test_make_default_keywords(self):
    '''keywords stemmed & unstemmed'''
    kw = KeywordWrapper()
    kw.load_text( self._sample_text )
    kw.set_top_num()
    kw.make_default_keywords()
    self.assertEqual( kw.keywords_stemmed[0:2], [(0.2222222222222222, u'dedic'), (0.18518518518518517, u'nation')] )
    self.assertEqual( kw.keywords_unstemmed[0:2], [(0.21739130434782608, u'nation'), (0.17391304347826086, u'dedicated')] )

  def test_make_additional_keywords(self):
    '''unstemmed words not in stemmed list'''
    kw = KeywordWrapper()
    kw.keywords_stemmed = [(0.1, u'courag'), (0.2, u'heart')]
    kw.keywords_unstemmed = [(0.3, u'courageous'), (0.4, u'brain')]
    kw.make_additional_keywords()
    self.assertEqual( kw.keywords_unstemmed_additional, [(0.4, u'brain')] )



  def test_make_additional_keywords_emptySource(self):
    kw = KeywordWrapper()
    kw.keywords_stemmed = []
    kw.keywords_unstemmed = []
    kw.make_additional_keywords()
    self.assertEqual( kw.keywords_unstemmed_additional, [] )



  def test_build_explore_json_string(self): 
    kw = KeywordWrapper()
    kw.load_text( self._sample_text ) 
    kw.set_top_num()
    kw.make_default_keywords() 
    kw.make_additional_keywords()
    kw.build_explore_json_string() 
    d = json.loads( kw.explore_json_string )
    self.assertEqual( sorted(d.keys()), [
      u'count_keywords_stemmed',
      u'count_keywords_unstemmed',
      u'count_keywords_unstemmed_additional',
      u'count_words_analyzed',
      u'count_words_raw',
      u'count_words_repeating_stemmed',
      u'count_words_repeating_unstemmed',
      u'docs',
      u'hash_md5',
      u'keywords_stemmed',
      u'keywords_unstemmed',
      u'keywords_unstemmed_additional',
      u'repeating_words_unstemmed',
      u'time_start',
      u'time_taken'] )

  def test_build_simple_json_string(self):
    kw = KeywordWrapper()
    kw.load_text( self._sample_text ) 
    kw.set_top_num()
    kw.make_keywords_stemmed_simple()
    kw.build_simple_json_string()
    d = json.loads( kw.simple_json_string )
    self.assertEqual( sorted(d.keys()), [
      u'count_keywords_stemmed',
      u'docs',
      u'hash_md5',
      u'keywords_stemmed',
      u'time_start',
      u'time_taken'] )


##
## test-runner call
##


if __name__ == "__main__":
  unittest.main()
