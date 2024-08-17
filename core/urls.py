from django.urls import path
from sentiment_analysis_app.views import analyze_sentiment

urlpatterns = [
    path("", analyze_sentiment, name="home"),
]
