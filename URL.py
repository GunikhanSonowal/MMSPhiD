from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
   
    url(r'^current_url/', 'secondproject.views.current_url', name='current_url'),
    url(r'^phonemCheck/', 'secondproject.views.phonemCheck', name='phonemCheck'),
    url(r'^moreinformation/', 'secondproject.views.moreinformation', name='moreinformation'),
    
    url(r'^typo/', 'secondproject.views.typo', name='typo'),
    url(r'^$', views.index, name='index'),
   
]    
    
