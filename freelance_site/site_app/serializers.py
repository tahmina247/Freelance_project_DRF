from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'avatar', 'bio', 'role', 'skills', 'social_links')
        extra_kwargs = {'passwords':{'write only':True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})

        if not user.is_active:
            raise serializers.ValidationError("Пользователь не активен")

        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'role', 'bio', 'avatar', 'skills', 'social_links']


class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'category_name']


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']



class ProjectListSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()

    class Meta:
        model = Project
        fields = ['id', 'title', 'category', 'description']


class ProjectDetailSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()
    client = SimpleUserSerializer()

    class Meta:
        model = Project
        fields = ['title', 'category', 'description', 'budget', 'deadline',
                  'status', 'skills_required', 'client', 'created_at']


class ProjectCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class OfferListSerializer(serializers.ModelSerializer):
    freelancer = SimpleUserSerializer()

    class Meta:
        model = Offer
        fields = ['id', 'project', 'freelancer', 'message']


class OfferDetailSerializer(serializers.ModelSerializer):
    freelancer = SimpleUserSerializer()

    class Meta:
        model = Offer
        fields = ['project', 'freelancer', 'message', 'proposed_budget', 'proposed_deadline', 'created_at']


class OfferCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    reviewer = SimpleUserSerializer()

    class Meta:
        model = Review
        fields =['id', 'project', 'reviewer', 'star']


class ReviewDetailSerializer(serializers.ModelSerializer):
    reviewer = SimpleUserSerializer()

    class Meta:
        model = Review
        fields =['project', 'reviewer', 'target', 'star', 'comment', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class CategoryDetailSerializer(serializers.ModelSerializer):
    projects = ProjectListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'projects']


