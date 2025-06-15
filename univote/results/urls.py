from django.urls import path
from . import views

urlpatterns = [
    path('', views.result_dashboard, name='result_dashboard'),
    path('election/<int:election_id>/', views.election_results, name='election_results'),
    path('election/<int:election_id>/pdf/', views.election_results_pdf, name='election_results_pdf'),
    path('election/<int:election_id>/export/', views.election_results_export, name='election_results_export'),
]