from rest_framework import viewsets, status, permissions, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from ..models import Survey, QualificationTest, SurveyResponse, RespondentQualification
from ..serializers import SurveySerializer, SurveyListSerializer, QualificationTestSerializer, SurveyResponseSerializer, RespondentQualificationSerializer
from django.db.models import F

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

@method_decorator(csrf_exempt, name='dispatch')
class SurveyViewSet(viewsets.ModelViewSet):
    """Survey CRUD operations"""
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Allow public retrieve, require auth for others

    def get_queryset(self):
        """
        Filter surveys by ownership for management actions.
        Allow retrieval by ID for survey taking.
        """
        user = self.request.user
        
        if self.action == 'list':
            if user.is_authenticated:
                return Survey.objects.filter(user=user).order_by('-created_at')
            return Survey.objects.none()
            
        # For retrieve, we allow everyone (to take the survey)
        if self.action == 'retrieve':
            return Survey.objects.all()
            
        # For updates/deletes/etc, restrict to owner
        if user.is_authenticated:
            return Survey.objects.filter(user=user).order_by('-created_at')
        return Survey.objects.none()

    def get_serializer_class(self):
        if self.action == 'list':
            return SurveyListSerializer
        return SurveySerializer

    def update(self, request, *args, **kwargs):
        """Allow partial updates for surveys"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        print(f"DEBUG: Survey Create - User: {self.request.user}, Auth: {self.request.user.is_authenticated}")
        print(f"DEBUG: Survey Create - Cookies: {self.request.COOKIES}")
        
        # Link to user if authenticated
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError({
                "detail": "You must be logged in to create a survey."
            })

    @action(detail=True, methods=['post'])
    def send_invite(self, request, pk=None):
        """Send email invitations for the survey"""
        from django.core.mail import send_mail
        from django.conf import settings
        
        try:
            survey = self.get_object() # Standard DRF method

            emails = request.data.get('emails', [])
            domain_restriction = request.data.get('domain_restriction', 'public')
            allowed_domain = request.data.get('allowed_domain', '')

            if not emails:
                return Response({'error': 'No emails provided'}, status=status.HTTP_400_BAD_REQUEST)

            # Update survey restrictions
            if domain_restriction == 'restricted' and allowed_domain:
                survey.allowed_domains = [allowed_domain]
            else:
                survey.allowed_domains = []
            
            survey.save()

            subject = f"You're invited to take a survey: {survey.title}"
            # TODO: Hardcoded localhost URL should be an env var
            message = f"Please click the link below to participate in the survey:\n\nhttp://localhost:8080/survey/{survey.id}\n\nThank you!"
            from_email = settings.EMAIL_HOST_USER
            
            send_mail(
                subject, message, from_email, emails, fail_silently=False,
            )
            
            return Response({'message': f'Invites sent successfully to {len(emails)} recipients'}, status=status.HTTP_200_OK)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({
                'error': 'Internal Server Error',
                'detail': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class QualificationTestViewSet(viewsets.ModelViewSet):
    """Qualification Test CRUD operations"""
    serializer_class = QualificationTestSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Allow retrieving specific qualification tests by survey ID for everyone (needed for respondents)
        survey_id = self.request.query_params.get('survey')
        if survey_id:
            return QualificationTest.objects.filter(survey_id=survey_id)

        # For listing all tests (dashboard view), restrict to owner
        user = self.request.user
        if not user.is_authenticated:
            return QualificationTest.objects.none()
            
        return QualificationTest.objects.filter(survey__user=user).order_by('-created_at')

    def update(self, request, *args, **kwargs):
        """Allow partial updates for qualification tests"""
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class SurveyResponseViewSet(viewsets.ModelViewSet):
    """Survey Response CRUD operations"""
    serializer_class = SurveyResponseSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            # Maybe allow public access if they have a specific token? 
            # For now, only owners see results.
            return SurveyResponse.objects.none()
            
        queryset = SurveyResponse.objects.filter(survey__user=user).order_by('-completed_at')
        survey_id = self.request.query_params.get('survey')
        if survey_id:
            queryset = queryset.filter(survey_id=survey_id)
        return queryset

    def perform_create(self, serializer):
        try:
            # Save first
            instance = serializer.save()
            
            # Then Audit Quality
            try:
                from ..ai_helper import analyze_response_quality
                
                if instance.survey:
                    questions = instance.survey.questions
                    # Analyze
                    audit_result = analyze_response_quality(questions, instance.responses)
                    
                    # Update instance
                    instance.quality_score = audit_result.get('score', 100)
                    instance.quality_analysis = audit_result
                    instance.is_flagged = instance.quality_score < 60
                    instance.save()
                
            except Exception as e:
                print(f"Error during Quality Audit: {e}")

        except Exception as e:
            raise e

@method_decorator(csrf_exempt, name='dispatch')
class RespondentQualificationViewSet(viewsets.ModelViewSet):
    """Respondent Qualification CRUD operations"""
    serializer_class = RespondentQualificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return RespondentQualification.objects.filter(survey__user=user).order_by('-created_at')
