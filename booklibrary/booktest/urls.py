from django.conf.urls import url
from . import views
app_name = 'booktest'
urlpatterns = [
    url(r'^index/$',views.index,name='index'),
    url(r'^rlogin/$',views.rlogin,name='rlogin'),
    url(r'^mlogin/$',views.mlogin,name='mlogin'),
    url(r'^register/$',views.register,name='register'),
    # url(r'^register1/$',views.register1,name='register1'),
    url(r'^logout/$',views.logout,name='logout'),
    url(r'^histroy/$',views.histroy,name='histroy'),
    url(r'^info/$',views.info,name='info'),
    url(r'^query/(\d+)/$',views.query,name='query'),
    url(r'^book/(\d+)/$',views.book,name='book'),
    url(r'^reader/$', views.reader, name='reader'),
    url(r'^upload/$',views.upload,name='upload'),
    url(r'^edit/$',views.edit,name='edit'),
    url(r'^meilto/$',views.meilto,name='meilto'),
    url(r'^active/(.*?)/$',views.active,name='active'),
    url(r'^ajax/$',views.ajax,name='ajax'),
    url(r'^ajaxajax/$',views.ajaxajax,name='ajaxajax'),

    url(r'^ajaxlogin/$',views.ajaxlogin,name='ajaxlogin'),
    url(r'^checkuser/$',views.checkuser,name='checkuser'),
    url(r'^verifycode/$',views.verifycode,name='verifycode'),

]