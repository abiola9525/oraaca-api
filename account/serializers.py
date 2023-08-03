from rest_framework import serializers
from . models import User, Student, Instructor
# Warehousemanager, Shelfmanager, Cashier

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_instructor', 'is_student']
        
        
        
 ################################       
        
class InstructorSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})
        
        user.set_password(password)
        user.is_instructor = True
        user.save()
        Instructor.objects.create(user=user)
        return user
           
class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model= Instructor
        fields= '__all__'      



class StudentSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match"})       
        user.set_password(password)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user
           
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model= Student
        fields= '__all__'  
        
        
class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)