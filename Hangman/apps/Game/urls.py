from django.conf.urls import url
from . import views

urlpatterns= [
    url(r'^$', views.loading),
    url(r'^guess$', views.guess),
    url(r'^reset$', views.reset),
    url(r'^begin$', views.begin),
    url(r'^gameover$', views.gameover),
    url(r'^game$', views.index)
]
