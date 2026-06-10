from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Utilisateur, Classe


class ClasseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classe
        fields = ['id', 'nom', 'niveau']


class UtilisateurSerializer(serializers.ModelSerializer):
    classe_details = ClasseSerializer(source='classe', read_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            'id', 'nom', 'prenom', 'email',
            'role', 'telephone', 'classe',
            'classe_details', 'date_creation'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=4)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            'email', 'password', 'password_confirm',
            'nom', 'prenom', 'role', 'telephone', 'classe'
        ]

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError(
                {'password': 'Les mots de passe ne correspondent pas'}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = Utilisateur(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError(
                'Email ou mot de passe incorrect'
            )
        if not user.is_active:
            raise serializers.ValidationError('Compte désactivé')
        data['user'] = user
        return data