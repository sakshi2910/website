
from django.conf.urls import include,url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about$', views.about, name='about'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^help$', views.help, name='help'),
    url(r'^all_news$', views.all_news, name='all_news'),
    url(r'^admission$', views.admission, name='admission'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/', include('login.urls')),
]
