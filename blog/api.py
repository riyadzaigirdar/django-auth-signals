from blog import serializers
from blog import models
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import base64

User = get_user_model()

@api_view(["GET", "POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def blog_list_view(request):
    # token = request.headers.get("Authorization")
    # authorized = False

    # if token:
    #     token = token.split(" ")[1]
    #     if Token.objects.filter(key=token).exists():
    #         authorized = True
    
    # if authorized:    
    if request.method == "GET":
        return Response(serializers.BlogPostSerializer(models.BlogPost.objects.all(), many = True).data, status=status.HTTP_200_OK)
    if request.method == "POST":
        request.data["author"] = User.objects.get(username="riyad").pk
        serializer = serializers.BlogPostSaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ok = {
                "username": User.objects.get(pk=serializer.data["author"]).username,
                "email": User.objects.get(pk=serializer.data["author"]).email
            }
            return Response({**serializer.data, "author": ok}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    # else:
    #     return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
@api_view(["GET", "PATCH", "DELETE"])
def blog_detail_view(request, slug):
    if request.method == "GET":
        serializer = serializers.BlogPostSerializer(models.BlogPost.objects.get(slug=slug))
        return Response(serializer.data, status = status.HTTP_200_OK)
    if request.method == "PATCH":
        serializer = serializers.BlogPostSerializer(models.BlogPost.objects.get(slug=slug), request.data)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        models.BlogPost.objects.get(slug=slug).delete()
        return Response({"message": "Post Deleted"}, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(type(token))
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        })