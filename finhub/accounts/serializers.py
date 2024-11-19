from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

# 회원가입용 커스텀 RegisterSerializer
class CustomRegisterSerializer(RegisterSerializer):
    age = serializers.IntegerField(required=False)
    capital = serializers.IntegerField(required=False)
    sido = serializers.CharField(max_length=10, required=False)
    sigungus = serializers.CharField(max_length=10, required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data.update({
            'nickname': self.validated_data.get('nickname', ""),
            'age': self.validated_data.get('age', 0),
            'capital': self.validated_data.get('capital', 0),
            'sido': self.validated_data.get('sido', ''),
            'sigungus': self.validated_data.get('sigungus', ''),
        })
        return data

    def save(self, request):
        user = super().save(request)
        user.age = self.validated_data.get('age', None)
        user.capital = self.validated_data.get('capital', None)
        user.nickname = self.validated_data.get('nickname', "")
        user.sido = self.validated_data.get('sido', '')
        user.sigungus = self.validated_data.get('sigungus', '')
        user.save()
        return user


# 사용자 정보 반환용 CustomUserDetailsSerializer
class CustomUserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', "nickname",'age', 'capital', 'sido', 'sigungus']
