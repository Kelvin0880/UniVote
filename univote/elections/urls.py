from django.urls import path
from . import views

urlpatterns = [
    path('', views.election_list, name='election_list'),
    path('create/', views.election_create, name='election_create'),
    path('<int:election_id>/', views.election_detail, name='election_detail'),
    path('<int:election_id>/edit/', views.election_edit, name='election_edit'),
    path('<int:election_id>/delete/', views.election_delete, name='election_delete'),
    path('candidates/create/', views.candidate_create, name='candidate_create'),
    path('candidates/<int:candidate_id>/edit/', views.candidate_edit, name='candidate_edit'),
    path('candidates/<int:candidate_id>/delete/', views.candidate_delete, name='candidate_delete'),
    path('<int:election_id>/vote/', views.vote, name='vote'),
]