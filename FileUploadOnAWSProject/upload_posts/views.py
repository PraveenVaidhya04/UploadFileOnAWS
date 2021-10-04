from .models import Posts
from .serializer import GetAllPostsSerializer, UploadPostsSerializers, GetOwnPostsSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from FileUploadOnAWSProject.tokens import CsrfExemptSessionAuthentication


class GetAllPostsView(APIView):

    def get(self, request):
        data = {}
        get_posts_data = Posts.objects.all().order_by("-id")
        get_data = GetAllPostsSerializer(get_posts_data, many=True)
        post_data = get_data.data

        data['detail'] = "Get all posts."
        data['status'] = 1
        data['data'] = post_data
        return Response(data)


class UploadPostsView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            serializer = UploadPostsSerializers(request, data=request.data)
            data = {}
            if serializer.is_valid():
                url = settings.BASE_URL + 'posts/view-posts/' + str(serializer.validated_data.id)
                Posts.objects.filter(id=serializer.validated_data.id).update(url=url)

                data['detail'] = "Post Upload Successfully."
                data['status'] = 1
                data['post_url'] = settings.BASE_URL + 'posts/view-posts/' + str(serializer.validated_data.id)
                return Response(data)


class ViewPostsView(APIView):

    def get(self, request, id):
        data = {}
        get_posts_data = Posts.objects.filter(id=id).order_by("-id")
        get_data = GetAllPostsSerializer(get_posts_data, many=True)
        post_data = get_data.data

        data['detail'] = "Get Post."
        data['status'] = 1
        data['data'] = post_data
        return Response(data)


class ViewOwnPostsView(APIView):
    authentication_classes = (TokenAuthentication, CsrfExemptSessionAuthentication, BasicAuthentication,)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.method == "POST":
            serializer = GetOwnPostsSerializers(request, data=request.data)
            if serializer.is_valid():
                data = {}
                get_posts_data = Posts.objects.filter(created_by=serializer.validated_data).order_by("-id")
                get_data = GetAllPostsSerializer(get_posts_data, many=True)
                post_data = get_data.data

                data['detail'] = "Get all posts."
                data['status'] = 1
                data['data'] = post_data
                return Response(data)