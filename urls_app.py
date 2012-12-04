# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *
# from django.views.generic.simple import redirect_to


urlpatterns = patterns( '',

  ( r'^about/$',  'nlp_app.views.about' ),
  
  ( r'^keywords/form/$',  'nlp_app.views.keyword_form' ),
  
  ( r'^keywords/$',  'nlp_app.views.keywords' ),

  ( r'^keywords2/$',  'nlp_app.views.keywords2' ),
    
  )
