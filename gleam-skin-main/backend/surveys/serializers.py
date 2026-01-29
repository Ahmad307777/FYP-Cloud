from rest_framework import serializers
from .models import Survey, QualificationTest, SurveyResponse, RespondentQualification

class SurveySerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')
    response_count = serializers.IntegerField(source='response_counter', read_only=True)
    question_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Survey
        fields = [
            'id', 'user_id', 'title', 'description', 'template', 
            'questions', 'require_qualification', 'qualification_pass_score', 
            'allowed_domains', 'design', 'created_at', 'updated_at', 
            'response_count', 'question_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user']

    def get_question_count(self, obj):
        if isinstance(obj.questions, list):
            return len(obj.questions)
        return 0

class SurveyListSerializer(serializers.ModelSerializer):
    """Lighter serializer for list view"""
    user_id = serializers.ReadOnlyField(source='user.id')
    response_count = serializers.IntegerField(source='response_counter', read_only=True)
    question_count = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = [
            'id', 'user_id', 'title', 'description', 'template', 
            'require_qualification', 'created_at', 'updated_at', 
            'response_count', 'question_count'
        ]

    def get_question_count(self, obj):
        if isinstance(obj.questions, list):
            return len(obj.questions)
        return 0

class QualificationTestSerializer(serializers.ModelSerializer):
    survey_id = serializers.PrimaryKeyRelatedField(
        queryset=Survey.objects.all(), source='survey', write_only=True
    )
    survey = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = QualificationTest
        fields = ['id', 'survey', 'survey_id', 'topic', 'questions', 'time_limit', 'created_at']

class SurveyResponseSerializer(serializers.ModelSerializer):
    survey_id = serializers.PrimaryKeyRelatedField(
        queryset=Survey.objects.all(), source='survey', write_only=True
    )
    survey = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SurveyResponse
        fields = [
            'id', 'survey', 'survey_id', 'respondent_email', 'responses', 
            'completed_at', 'quality_score', 'quality_analysis', 'is_flagged'
        ]
        read_only_fields = ['completed_at', 'quality_score', 'quality_analysis', 'is_flagged']

class RespondentQualificationSerializer(serializers.ModelSerializer):
    survey_id = serializers.PrimaryKeyRelatedField(
        queryset=Survey.objects.all(), source='survey', write_only=True
    )
    survey = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = RespondentQualification
        fields = [
            'id', 'survey', 'survey_id', 'respondent_email', 
            'qualification_name', 'score', 'passed', 'created_at'
        ]
        read_only_fields = ['created_at']
