from django.urls import path
from .views import analysis_history

urlpatterns = [
    path("history/", analysis_history, name="analysis_history"),
]
