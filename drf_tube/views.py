from django.shortcuts import render
from uzbektube.models import *
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CategoriesSerializer, ContentListSerializer, ContentDetailSerializer, CommentCreateSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def category_list_view(request):
    categories = Category.objects.all()
    serializer = CategoriesSerializer(categories, many=True)

    if request.method == 'POST':
        serializer = CategoriesSerializer(data=request.data)
        serializer.is_valid()
        serializer.save()

    return Response(serializer.data)


@api_view()
def content_list_view(request):
    contents = VideoContent.objects.all().annotate(
        count_views=models.Count(models.F('views'))
    ).order_by('-created_ad')
    serializer = ContentListSerializer(contents, many=True)
    return Response(serializer.data)

@api_view()
def content_by_category(request, pk):
    contents = VideoContent.objects.filter(category=pk).annotate(
        count_views=models.Count(models.F('views'))
    ).order_by('-created_ad')
    serializer = ContentListSerializer(contents, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def content_detail(request, pk):
    content = VideoContent.objects.annotate(
        count_views=models.Count(models.F('views'))
    ).get(pk=pk)

    if request.method == 'POST' and request.user.is_authenticated:
        data = request.data
        data['user_id'] = request.user.id
        data['content_id'] = content.id
        serializer = CommentCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    serializer = ContentDetailSerializer(content)
    return Response(serializer.data)



# Вьюшка отдельная и отдельная API дял добавления коммента
@api_view(['POST'])
def comment_create(request):

    if request.method == 'POST':
        data = request.data
        data['user_id'] = request.user.id
        serializer = CommentCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)