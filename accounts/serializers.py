from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        max_length=30,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'nickname', 'email')
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password1 = serializers.CharField(write_only=True, required=True)
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("기존 비밀번호가 올바르지 않습니다.")
        return value
    
    def validate(self, attrs):
        pw1 = attrs.get("new_password1")
        pw2 = attrs.get("new_password2")
        if pw1 != pw2:
            raise serializers.ValidationError("새 비밀번호가 일치하지 않습니다.")
        
        user = self.context['request'].user
        if user.check_password(pw1):
            raise serializers.ValidationError("기존 비밀번호와 동일합니다.")
        
        password_validation.validate_password(pw1, user=user)
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password1'])
        user.save()
        return user