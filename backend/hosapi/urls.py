from hosapi import views
from django.conf.urls import url


urlpatterns = [
    url(r'^userlog/', views.authenticate_user),
    url(r'^signup/', views.signup),
    url(r'^hospuser_data/all/', views.hospusers_data_all),
    url(r'^subjectsall', views.get_subjects),
    url(r'^samplessall/', views.get_samples),
    url(r'^hospuser_data/update/', views.update_hospuser),
    url(r'^subjectupdate/', views.update_subjects),
    url(r'^subjectdelete/', views.delete_subjects),
    url(r'^sampleupdate/', views.update_samples),
    url(r'^sampledelete/', views.delete_samples),
    url(r'^hospuser_data/(?P<username>[^/]+)/?$', views.hospuser_data),
    url(r'^subjectcreation/', views.createsubject),
    url(r'^samplecreation/', views.createsample),
 ]