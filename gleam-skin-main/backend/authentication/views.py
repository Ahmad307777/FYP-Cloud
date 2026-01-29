from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
import re
import sys

def validate_email(email):
    """Simple email validation"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """User login endpoint using Django Auth"""
    try:
        # Use DRF's request.data which handles JSON automatically
        data = request.data
        username = data.get('username', '').strip() or data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        print(f"DEBUG: Login Attempt - Raw Username/Email: '{username}'", flush=True)
        
        # Check database state
        user_count = User.objects.count()
        print(f"DEBUG: Total Users in DB: {user_count}", flush=True)
        
        actual_username = username
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                actual_username = user_obj.username
                print(f"DEBUG: Found user by email. Actual username: '{actual_username}'")
            except User.DoesNotExist:
                print(f"DEBUG: No user found with email: '{username}'")
                # Fallback to authenticating with the email as username just in case
                pass
            except User.MultipleObjectsReturned:
                print(f"DEBUG: Multiple users found with email: '{username}'")
                user_obj = User.objects.filter(email=username).first()
                actual_username = user_obj.username

        # Check if user exists before authenticating
        exists = User.objects.filter(username=actual_username).exists()
        print(f"DEBUG: User '{actual_username}' exists in DB: {exists}")

        user = authenticate(request, username=actual_username, password=password)

        if user is not None:
            login(request, user)
            print(f"DEBUG: Login Success - User ID: {user.id}")
            return Response({
                'detail': 'Logged in successfully',
                'user': {'id': user.id, 'username': user.username, 'email': user.email}
            })
        else:
            print(f"DEBUG: Login Failed - Authentication failed for user '{actual_username}'")
            return Response({'detail': 'Invalid credentials', 'error': True}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'detail': f'Login error: {str(e)}', 'error': True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_view(request):
    """User registration endpoint using Django Auth"""
    try:
        # Use DRF's request.data which handles JSON automatically
        data = request.data
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()

        print(f"DEBUG: Register Attempt - Username: '{username}', Email: '{email}'", flush=True)

        if not username or not email or not password:
            return Response({'detail': 'All fields are required', 'error': True}, status=status.HTTP_400_BAD_REQUEST)

        # Sanitize username: Django's default User model doesn't allow spaces.
        sanitized_username = username.replace(' ', '_')
        if sanitized_username != username:
            print(f"DEBUG: Sanitized username '{username}' to '{sanitized_username}'", flush=True)
            username = sanitized_username

        if User.objects.filter(username=username).exists():
            return Response({'detail': 'Username already exists', 'error': True}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'detail': 'Email already exists', 'error': True}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return Response({
                'detail': 'Registered and logged in successfully',
                'user': {'id': user.id, 'username': user.username, 'email': user.email}
            }, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'detail': 'Registration failed (Database error)', 'error': True}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'detail': f'Registration error: {str(e)}', 'error': True}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def logout_view(request):
    """User logout endpoint"""
    try:
        logout(request)
        return Response({'detail': 'Logged out successfully'})
    except Exception as e:
        return Response({
            'detail': f'Logout error: {str(e)}',
            'error': True
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_view(request):
    """Get current user info"""
    print(f"DEBUG: Get User - User: {request.user}, Auth: {request.user.is_authenticated}")
    print(f"DEBUG: Get User - Cookies: {request.COOKIES}")
    try:
        if request.user.is_authenticated:
            return Response({
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email
                }
            })
        return Response({'user': None})
    except Exception as e:
        return Response({
            'detail': f'Error: {str(e)}',
            'error': True
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
