from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from .models import Account, WorkingHistory


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=28, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=28, write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'role', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError({'success': False, 'message': "Parol mos kelmadi, qayta urinib ko'ring"})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, max_length=88, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        email = obj.get('email')
        print(email)
        tokens = Account.objects.get(email=email).tokens
        print(Account.objects.get(email=email).role)
        print(tokens)
        return tokens

    class Meta:
        model = Account
        fields = ('email', 'password', 'tokens')

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed({
                "message": 'Email yoki Parol xato'
            })
        if not user.is_active:
            raise AuthenticationFailed({
                'message': 'Account faol emas'
            })
        return attrs


class MyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'full_name', 'image_url', 'role', 'get_role_display', 'bio', 'modified_date', 'created_date')


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'full_name', 'image', 'role', 'get_role_display', 'bio', 'modified_date', 'created_date')
        extra_kwargs = {
            'email': {'required': False},
            'role': {'read_only': True},
            'bio': {'required': False},
            'image': {'required': False},
        }


class WorkingHistoryGETSerializer(serializers.ModelSerializer):
    account = MyAccountSerializer(read_only=True)

    class Meta:
        model = WorkingHistory
        fields = ('id', 'account', 'company', 'location', 'start_date', 'end_date', 'is_current')


class WorkingHistoryPOSTSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkingHistory
        fields = ('id', 'account', 'company', 'location', 'start_date', 'end_date', 'is_current')

    def validate(self, attrs):
        account = attrs.get('account')
        if account.role == 0:
            raise ValidationError('Candidate work history post qila oladi')
        if account.role == 2:
            raise ValidationError('Candidate work history post qila oladi')
        return attrs







