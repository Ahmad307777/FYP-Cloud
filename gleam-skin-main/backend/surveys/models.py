from django.db import models
from django.conf import settings
from django.utils import timezone

class Survey(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    template = models.CharField(max_length=255, blank=True, null=True)
    questions = models.JSONField(default=list)  # List of question dictionaries
    require_qualification = models.BooleanField(default=False)
    qualification_pass_score = models.IntegerField(blank=True, null=True)
    allowed_domains = models.JSONField(default=list)  # List of strings
    design = models.JSONField(default=dict) # Visual customization
    response_counter = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return self.title

class QualificationTest(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='qualification_tests')
    topic = models.CharField(max_length=255)
    questions = models.JSONField(default=list)
    time_limit = models.IntegerField(default=0) # Minutes
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Test for {self.survey.title}"

class SurveyResponse(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    respondent_email = models.EmailField()
    responses = models.JSONField(default=dict) # key-value pairs of answers
    completed_at = models.DateTimeField(default=timezone.now)

    # Quality Control
    quality_score = models.IntegerField(default=100)
    quality_analysis = models.JSONField(default=dict)
    is_flagged = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['survey', 'respondent_email']),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and self.survey:
            # Atomic increment
            # Note: In SQL we can use F expressions but for simplicity we keep it close to logic
            from django.db.models import F
            Survey.objects.filter(id=self.survey.id).update(response_counter=F('response_counter') + 1)

    def delete(self, *args, **kwargs):
        survey_id = self.survey_id
        super().delete(*args, **kwargs)
        if survey_id:
             from django.db.models import F
             Survey.objects.filter(id=survey_id).update(response_counter=F('response_counter') - 1)

    def __str__(self):
        return f"Response to {self.survey.title} by {self.respondent_email}"

class RespondentQualification(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    respondent_email = models.EmailField()
    qualification_name = models.CharField(max_length=255, blank=True, null=True)
    score = models.IntegerField()
    passed = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.respondent_email} - {self.score} ({'Passed' if self.passed else 'Failed'})"

