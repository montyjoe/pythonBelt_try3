from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^appointments$', views.appointments),
    url(r'^add_appointment$', views.add_appointment),
    url(r'^appointments/(?P<appointment_id>\d+)$', views.update_page, name="update_page"),
    url(r'^update$', views.update),
    url(r'^appointments/(?P<appointment_id>\d+)/delete$', views.delete),

]
