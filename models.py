# -*- coding: utf-8 -*-

import datetime, json, unittest
from types import NoneType

import nlp_app_settings as app_settings
import pattern
from pattern.vector import Document, PORTER, stem


## 
## non-django models
##


class KeywordWrapper( object ):

  time_start = None
  original_text = None
  document_raw = None
  document_raw_count = None
  document_thresh_stemmed = None
  # document_thresh_stemmed_count = None
  document_thresh_unstemmed = None
  # document_thresh_unstemmed_count = None
  top_num = 10
  keywords_stemmed = None
  keywords_unstemmed = None
  keywords_unstemmed_additional = None
  json_string = None

  def load_text( self, text ):
    self.time_start = datetime.datetime.now()
    self.document_raw = Document( text, threshold=0 )
    self.document_raw_count = self.document_raw.count
    self.document_thresh_stemmed = Document( text, stemmer=PORTER, threshold=1 )
    self.document_thresh_unstemmed = Document( text, threshold=1 )
    self.original_text = text

  def set_top_num( self ):
    assert type(self.document_raw) == pattern.vector.Document
    for i in range( 0, self.document_raw.count, 1000 ):
      self.top_num += 1
      if self.top_num == 50:
        break

  def make_default_keywords( self ):
    assert type(self.document_thresh_stemmed) == pattern.vector.Document
    assert type(self.document_thresh_unstemmed) == pattern.vector.Document
    self.keywords_stemmed = self.document_thresh_stemmed.keywords( top=self.top_num )
    self.keywords_unstemmed = self.document_thresh_unstemmed.keywords( top=self.top_num )
    
  def make_additional_keywords( self ):
    assert type(self.keywords_stemmed) == list;     assert type(self.keywords_stemmed[0]) == tuple
    assert type(self.keywords_unstemmed) == list;   assert type(self.keywords_stemmed[0]) == tuple
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

  def build_json_string( self ):
    d = {
      u'count_words_raw': len( self.original_text.split() ),
      u'count_words_analyzed': self.document_raw.count,
      u'count_words_repeating_stemmed': self.document_thresh_stemmed.count,
      u'count_words_repeating_unstemmed': self.document_thresh_unstemmed.count,
      u'count_keywords_stemmed': len( self.keywords_stemmed ),
      u'count_keywords_unstemmed': len( self.keywords_unstemmed ),
      u'count_keywords_unstemmed_additional': len( self.keywords_unstemmed_additional ),
      u'keywords_stemmed': self.keywords_stemmed,
      u'keywords_unstemmed': self.keywords_unstemmed,
      u'keywords_unstemmed_additional': self.keywords_unstemmed_additional,
      u'repeating_words_unstemmed': self.document_thresh_unstemmed.terms,
      u'time_start': unicode( self.time_start ),
      u'time_taken': unicode( datetime.datetime.now() - self.time_start ),
      u'docs': app_settings.DOCS_URL
      }
    self.json_string = json.dumps( d, sort_keys=True, indent=2 )


##
## tests
##


class KeyWordWrapperTest( unittest.TestCase ):

  _sample_text = u'''
    Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal.
    Now we are engaged in a great civil war, testing whether that nation, or any nation, so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this.
    But, in a larger sense, we can not dedicate, we can not consecrate, we can not hallow this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us—that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion—that we here highly resolve that these dead shall not have died in vain—that this nation, under God, shall have a new birth of freedom—and that government of the people, by the people, for the people, shall not perish from the earth.
    '''

  def test_load_test(self):
    '''loads text & makes default document-objects: # raw, thresh-stemmed, thresh-unstemmed'''
    kw = KeywordWrapper()
    self.assertEqual( type(kw.document_raw), NoneType )
    kw.load_text( self._sample_text )
    self.assertEqual( type(kw.document_raw), pattern.vector.Document )
    self.assertEqual( kw.document_raw_count, 84 )

  def test_set_top_num(self):
    '''starts at 10; increases +1 every thousand words up to 50'''
    kw = KeywordWrapper()
    self.assertEqual( kw.top_num, 10 )
    kw.load_text( u'word ' * 10000 )
    kw.set_top_num()
    self.assertEqual( kw.document_raw.count, 10000 )
    self.assertEqual( kw.top_num, 20 )

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

  def test_build_json_string(self): 
    kw = KeywordWrapper()
    kw.load_text( self._sample_text ) 
    kw.set_top_num()
    kw.make_default_keywords() 
    kw.make_additional_keywords()
    kw.build_json_string() 
    d = json.loads( kw.json_string )
    self.assertEqual( d.keys(), [  
      u'count_words_analyzed', u'count_keywords_stemmed',
      u'repeating_words_unstemmed', u'keywords_unstemmed', u'docs',
      u'count_words_raw', u'keywords_unstemmed_additional',
      u'count_words_repeating_unstemmed', u'keywords_stemmed',
      u'count_words_repeating_stemmed', u'time_start', u'time_taken',
      u'count_keywords_unstemmed_additional', u'count_keywords_unstemmed'] 
      )

##
## test-runner call
##


if __name__ == "__main__":
  # ## setup
  # import usepi_ingest_settings as ui_settings
  # activate_this = u'%s/env/bin/activate_this.py' % ui_settings.PROJECT_DIR_PATH
  # # print u'- activate_this: '; print activate_this
  # execfile( activate_this, dict(__file__=activate_this) )
  # import lxml, solr
  # from lxml import etree
  # settings = {
  #   u'LOG_PATH': ui_settings.LOG_PATH,
  #   u'PRINT_LOG_OUTPUT': ui_settings.PRINT_LOG_OUTPUT,
  #   u'SOLR_URL': ui_settings.SOLR_URL,
  #   u'XML_BIB_PATH': ui_settings.XML_BIB_PATH,
  #   u'XML_DIR_PATH': ui_settings.XML_DIR_PATH,
  #   }
  # from usep_index_script import Parser, UsepIndexUpdater
  # updater = UsepIndexUpdater( settings )
  # print u'- here'
  ## test if desired
  unittest.main()  # when run, will prevent subsequent lines from executing (which is fine)
