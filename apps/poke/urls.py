from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login_reg$', views.login_reg),
    url(r'^dashboard$', views.dashboard),
    url(r'^log_out$', views.logout),
    url(r'poke$', views.poke)
]