from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Analysis


class AnalysisModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123"
        )
        self.analysis = Analysis.objects.create(
            user=self.user,
            input_text="I love this product!",
            polarity=0.9,
            subjectivity=0.6,
        )

    def test_analysis_creation(self):
        self.assertEqual(self.analysis.input_text, "I love this product!")
        self.assertEqual(self.analysis.polarity, 0.9)
        self.assertEqual(self.analysis.subjectivity, 0.6)
        self.assertEqual(self.analysis.user.username, "testuser")
