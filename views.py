# -*- coding: utf-8 -*-

import datetime, json
import pattern, requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response


def about( request ):
  info = {
    u'info': u'workspace for nlp experimentation with python module \'pattern\' (http://www.clips.ua.ac.be/pages/pattern)'
  }
  jstring = json.dumps( info, indent=2 )
  return HttpResponse( jstring, content_type=u'text/javascript; charset=utf8' )
  
  
def keywords( request ):
  from pattern.vector import Document, PORTER, stem
  start = datetime.datetime.now()
  try:
    t = request.GET[u'text']
  except KeyError:
    try:
      t = request.POST[u'text']
    except KeyError:
      return HttpResponseBadRequest( u'400 / Bad Request; no text parameter' )
  document_raw = Document( t, threshold=0 )
  document_thresh_stemmed = Document( t, stemmer=PORTER, threshold=1 )
  document_thresh_unstemmed = Document( t, threshold=1 )
  # add a keyword for every extra thousand words
  TOP_NUM = 10
  for i in range( 0, document_raw.count, 1000 ):
    TOP_NUM += 1
    if TOP_NUM == 50:
      break
  keywords_unstemmed = document_thresh_unstemmed.keywords( top=TOP_NUM )
  keywords_stemmed = document_thresh_stemmed.keywords( top=TOP_NUM )
  # make simple list of keywords_stemmed words
  keywords_stemmed_simple = []
  for kw in keywords_stemmed:
    score = kw[0]; word = kw[1]
    keywords_stemmed_simple.append( word )
  # look for additional keywords
  keywords_unstemmed_additional = []
  for kw in keywords_unstemmed:
    score = kw[0]; word = kw[1]
    if word not in keywords_stemmed_simple:  # TODO: time using sets here instead
      if stem( word, stemmer=PORTER ) not in keywords_stemmed_simple:
        keywords_unstemmed_additional.append( kw )
  d = {
    u'time_start': unicode(start),
    u'time_taken': unicode( datetime.datetime.now() - start ),
    u'count_words_total': document_raw.count,
    u'count_words_repeating_stemmed': document_thresh_stemmed.count,
    u'count_words_repeating_unstemmed': document_thresh_unstemmed.count,
    u'count_keywords_stemmed': len( keywords_stemmed ),
    u'count_keywords_unstemmed': len( keywords_unstemmed ),
    u'count_keywords_unstemmed_additional': len( keywords_unstemmed_additional ),
    u'keywords_stemmed': keywords_stemmed,
    u'keywords_unstemmed': keywords_unstemmed,
    u'keywords_unstemmed_additional': keywords_unstemmed_additional,
    u'repeating_words_unstemmed': document_thresh_unstemmed.terms,      
    }
  jstring = json.dumps( d, sort_keys=True, indent=2 )
  return HttpResponse( jstring, content_type=u'text/javascript; charset=utf8' )
  
    
def keyword_form( request ):
  if request.method == 'GET':
    page_dict = {}
    return render_to_response( 'nlp_app_templates/test_form.html', page_dict )
  else:  # POST
    t = request.POST[u'text']
    referrer = request.META['HTTP_REFERER']
    # print '- referrer:'; print referrer
    url = referrer[0:-5]  # removing 'form/'
    params = { u'text': t }
    r = requests.post( url, data=params )
    return HttpResponse( r.text, content_type=u'text/javascript; charset=utf8' )
  