from rest_framework import serializers
from rest_framework import exceptions
from .models import Posts
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import base64
from PIL import Image
from datetime import date


class GetAllPostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'


class UploadPostsSerializers(serializers.Serializer):
    user_id = serializers.CharField(style={"input_type": "text"}, write_only=True)
    title = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)
    file = serializers.CharField(style={"input_type": "text"}, write_only=True, required=False, allow_blank=True)

    def validate(self, data):
        user_id = data.get("user_id", "")
        title = data.get("title", "")
        file = data.get("file", "") # file should be in Base64 format.
        if User.objects.filter(id=user_id).exists():
            user_instance = get_object_or_404(User, pk=user_id)
            data = ContentFile(base64.b64decode(file))
            get_image = Image.open(data)
            filetype = get_image.format
            ext = filetype.lower()
            today_date = date.today()
            set_file_name = str(title) + str(today_date.day) + "_" + str(today_date.month) + "_" + str(
                today_date.year)
            file_name = set_file_name + "." + ext
            data = ContentFile(base64.b64decode(file), name=file_name)
            get_objects = Posts(title=title, file=data, created_by=user_instance)
            get_objects.save()
            return get_objects

        else:
            mes = "Invalid user id."
            raise exceptions.APIException(mes)


class GetOwnPostsSerializers(serializers.Serializer):
    user_id = serializers.CharField(style={"input_type": "text"}, write_only=True)

    def validate(self, data):
        user_id = data.get("user_id", "")
        if User.objects.filter(id=user_id).exists():
            user_instance = get_object_or_404(User, pk=user_id)
            return user_instance
        else:
            mes = "Invalid user id."
            raise exceptions.APIException(mes)