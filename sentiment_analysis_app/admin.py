from django.contrib import admin
from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "input_text",
        "polarity",
        "subjectivity",
        "analysis_date",
    )
    list_filter = ("user", "analysis_date")
    search_fields = ("input_text",)
