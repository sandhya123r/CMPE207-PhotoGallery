from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^login/$', views.match, name='login'),
    url(r'^Users/([1-9]+)/Album/([\w-]+)/$', views.upload_image, name='upload'),
    url(r'^Users/([1-9]+)/$', views.create_album, name='create_album'),
    url(r'^delete_image/', views.delete_image, name='delete_image'),
    url(r'^delete_album/$', views.delete_album, name='delete_album'),
]

