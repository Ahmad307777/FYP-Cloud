from django.contrib import admin
from .models import Survey, SurveyResponse, QualificationTest, RespondentQualification

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'response_counter', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'user')

@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ('survey', 'respondent_email', 'quality_score', 'is_flagged', 'completed_at')
    list_filter = ('is_flagged', 'completed_at', 'survey')
    search_fields = ('respondent_email', 'survey__title')

@admin.register(QualificationTest)
class QualificationTestAdmin(admin.ModelAdmin):
    list_display = ('survey', 'topic', 'time_limit', 'created_at')

@admin.register(RespondentQualification)
class RespondentQualificationAdmin(admin.ModelAdmin):
    list_display = ('respondent_email', 'survey', 'score', 'passed', 'created_at')
    list_filter = ('passed', 'survey')
