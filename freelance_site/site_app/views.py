from rest_framework import viewsets, generics, status
from urllib3 import request

from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProjectFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import ProjectSetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import CheckOfferUser, CheckClientUser, CheckEditOfferUser


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail':' неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetailAPIView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer


class ProjectAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProjectFilter
    search_fields = ['title', 'skills_required']
    ordering_fields = ['budget', 'created_at', 'deadline']
    pagination_class = ProjectSetPagination


class ProjectDetailAPIView(generics.RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer


class ProjectPostApiView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [CheckClientUser]

    def get_queryset(self):
        return Project.objects.filter(client=self.request.user)


class ProjectEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectCreateSerializer
    permission_classes = [CheckClientUser]

    def get_queryset(self):
        return Project.objects.filter(client=self.request.user)


class ProjectDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [CheckClientUser]

    def get_queryset(self):
        return Project.objects.filter(client=self.request.user)


class ProjectMyAPIView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectListSerializer
    permission_classes = [CheckClientUser]

    def get_queryset(self):
        return Project.objects.filter(client=self.request.user)


class OfferListAPIView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferListSerializer


class OfferDetailAPIView(generics.RetrieveAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer



class OfferCreateAPIView(generics.ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer
    permission_classes = [CheckOfferUser]

    def get_queryset(self):
        return Offer.objects.filter(freelancer=self.request.user)



class OfferEditAPIView(generics.RetrieveUpdateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer
    permission_classes = [CheckOfferUser, CheckEditOfferUser]

    def get_queryset(self):
        return Offer.objects.filter(freelancer=self.request.user)



class OfferDeleteAPIView(generics.RetrieveDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferDetailSerializer
    permission_classes = [CheckOfferUser, CheckEditOfferUser]

    def get_queryset(self):
        return Offer.objects.filter(freelancer=self.request.user)



class OfferListMyAPIView(generics.ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferListSerializer
    permission_classes = [CheckOfferUser, CheckEditOfferUser]

    def get_queryset(self):
        return Offer.objects.filter(freelancer=self.request.user)


class ReviewAPIView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer


class ReviewDetailAPIView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer


class ReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [CheckOfferUser]

    def get_queryset(self):
        return Offer.objects.filter(freelancer=self.request.user)


