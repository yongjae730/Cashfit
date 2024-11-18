from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'age', 'capital']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            age=validated_data.get('age'),
            capital=validated_data.get('capital'),
        )
        user.set_password(validated_data['password'])  # 비밀번호 암호화
        user.save()
        return user
