# -*- coding: utf-8 -*-

import datetime, json

import nlp_app_settings as app_settings
assert dir(app_settings)[0:-5] == [u'DOCS_URL']  # rest all built-ins
import pattern, requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response


def about( request ):
  info = {
    u'docs': app_settings.DOCS_URL,
    u'info': u'workspace for nlp experimentation with python module \'pattern\' (http://www.clips.ua.ac.be/pages/pattern)'
  }
  jstring = json.dumps( info, indent=2 )
  return HttpResponse( jstring, content_type=u'text/javascript; charset=utf8' )


def keywords( request ):
  from nlp_app.models import KeywordWrapper  # non-django class; wrapper around 'pattern' module
  kw = KeywordWrapper()
  kw.get_params( request );  assert type(kw.params) == dict
  # print u'- params: %s' % kw.params
  if not u'text' in kw.params.keys():
    return HttpResponseBadRequest( u'400 / Bad Request; no text parameter' )
  else:
    kw.load_text( kw.params[u'text'] )  # loads text & makes default document-objects: # raw, thresh-stemmed, thresh-unstemmed
    kw.set_top_num()  # calculates number of keywords to return, based on text length
  if u'explore' in kw.params.keys() and kw.params[u'explore'] == u'true':
    kw.make_default_keywords()  # keyword-tuples, stemmed & unstemmed
    kw.make_additional_keywords()  # unstemmed keywords (tuples) not in stemmed list
    kw.build_explore_json_string()
    return HttpResponse( kw.explore_json_string, content_type=u'text/javascript; charset=utf8' )
  else:  # return simple unstemmed keyword list
    kw.make_keywords_stemmed_simple()
    kw.build_simple_json_string()
    return HttpResponse( kw.simple_json_string, content_type=u'text/javascript; charset=utf8' )


# def keywords( request ):
#   from nlp_app.models import KeywordWrapper  # non-django class; wrapper around 'pattern' module
#   try:
#     t = request.GET[u'text']
#   except KeyError:
#     try:
#       t = request.POST[u'text']
#     except KeyError:
#       return HttpResponseBadRequest( u'400 / Bad Request; no text parameter' )
#   kw = KeywordWrapper()
#   kw.load_text( t )  # loads text & makes default document-objects: # raw, thresh-stemmed, thresh-unstemmed
#   kw.set_top_num()  # calculates number of keywords to return, based on text length
#   kw.make_default_keywords()  # keyword-tuples, stemmed & unstemmed
#   kw.make_additional_keywords()  # unstemmed keywords (tuples) not in stemmed list
#   kw.build_json_string()
#   return HttpResponse( kw.json_string, content_type=u'text/javascript; charset=utf8' )
    
    
def keyword_form( request ):
  if request.method == u'GET':
    page_dict = {}
    return render_to_response( u'nlp_app_templates/test_form.html', page_dict )
  else:  # POST
    t = request.POST[u'text']
    referrer = request.META[u'HTTP_REFERER']
    # print '- referrer:'; print referrer
    url = referrer[0:-5]  # removing 'form/'
    params = { u'text': t, u'explore':u'true' }
    r = requests.post( url, data=params )
    return HttpResponse( r.text, content_type=u'text/javascript; charset=utf8' )
  
