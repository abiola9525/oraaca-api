from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from . models import Instructor, Student, User
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from . permissions import IsInstructorUser, IsStudentUser
from . serializers import UserSerializer, InstructorSignupSerializer,InstructorSerializer, StudentSignupSerializer ,ChangePasswordSerializer, StudentSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated  


# Create your views here.
class InstructorSignupView(generics.GenericAPIView):
    serializer_class=InstructorSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"Instuctor Account Created Successfully"
            })
        
    def get(self, request):
        user = Instructor.objects.all()
        serializer = InstructorSerializer(user, many=True)
        return Response(serializer.data)

@swagger_auto_schema(method='POST', operation_description='Retrieve a list of items with their associated foreign keys.', request_body=InstructorSerializer)
@api_view(['POST'])
def instructor_profile(request):
    if request.method == 'POST':
        serializer = InstructorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class StudentSignupView(generics.GenericAPIView):
    serializer_class=StudentSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"Student Account Created Successfully"
            })
        
    def get(self, request):
        user = Student.objects.all()
        serializer = StudentSerializer(user, many=True)
        return Response(serializer.data)

@swagger_auto_schema(method='PUT', operation_description='Retrieve a list of items with their associated foreign keys.', request_body=StudentSerializer)
@api_view(['PUT'])
def student_profile(request):
    if request.method == 'PUT':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        token, created=Token.objects.get_or_create(user=user)
        response_data = ({
            'token':token.key,
            'user_id':user.pk,
            'is_instructor':user.is_instructor,
            'is_student':user.is_student
        })        
        if user.is_instructor:
            response_data['redirect_to'] = '/instructor_dashboard/'  # Customize the URL for instructor dashboard
        elif user.is_student:
            response_data['redirect_to'] = '/student_dashboard/'  # Customize the URL for student dashboard
        else:
            response_data['redirect_to'] = '/login/'  # Redirect to a default page for other roles or handle as needed

        return Response(response_data)
        
        
        
class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)
    
class InstructorOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsInstructorUser]
    serializer_class=UserSerializer
    
    def get_object(self):
        return self.request.user
    
class StudentOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsStudentUser]
    serializer_class=UserSerializer
    
    def get_object(self):
        return self.request.user
    

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    