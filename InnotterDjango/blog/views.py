from django.shortcuts import render
from rest_framework import viewsets
from blog.serializers import TagSerializer, PageSerializer, PostSerializer
from blog.models import Tag, Page, Post


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    queryset = Page.objects.all()


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
