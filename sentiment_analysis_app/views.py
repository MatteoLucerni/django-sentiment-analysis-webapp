from django.shortcuts import render
from textblob import TextBlob
from .models import Analysis
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def analyze_sentiment(request):
    sentiment = None
    polarity = None
    subjectivity = None

    if request.method == "POST":
        user_input = request.POST.get("user_input")
        if user_input:

            # TextBlob sentiment analysis
            blob = TextBlob(user_input)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            sentiment = (
                "Positive"
                if polarity > 0
                else "Negative" if polarity < 0 else "Neutral"
            )

    return render(
        request,
        "core/home.html",
        {
            "sentiment": sentiment,
            "polarity": polarity,
            "subjectivity": subjectivity,
            "user_input": user_input,
        },
    )
