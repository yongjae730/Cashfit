from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username','password', 'age', 'capital','sido','sigungus']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            age=validated_data.get('age'),
            capital=validated_data.get('capital'),
            sido=validated_data.get('sido'),
            sigungus=validated_data.get('sigungus'),
        )
        user.set_password(validated_data['password'])  # 비밀번호 암호화
        user.save()
        return user
