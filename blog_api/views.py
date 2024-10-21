from rest_framework import generics, filters, permissions
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from blog.models import Post
from blog_api.serializers import PostSerializer
from blog_api.permissions import IsAthorOrReadOnly


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['author']
    search_fields = ['body', 'author__profile__bio']
    ordering_fields = ['author__id', 'publish']
    ordering_fields = '__all__'
    ordering = ['body']
    pagination_class = StandardResultsSetPagination

    # def get_queryset(self):
    #     user = self.request.user
    #     return Post.objects.filter(author=user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.IsAdminUser,)
    permission_classes = (IsAthorOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class UserPostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.kwargs['id']
        return Post.objects.filter(author=user)


###############################################################################
# Представления на основе APIView
###############################################################################

# from django.http import Http404

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from blog.models import Post
# from blog_api.serializers import PostSerializer


# class PostList(APIView):
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, format=None):
#         serializer =PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(id=pk)
#         except Post.DoesNotExist:
#             raise Http404
        
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patch(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(
#             post,
#             data=request.data,
#             partial=True
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         queryset = self.get_object(pk)
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


###############################################################################
# Представления на основе миксинов
###############################################################################

# from rest_framework import mixins
# from rest_framework import generics

# from blog.models import Post
# from blog_api.serializers import PostSerializer


# class PostList(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class PostDetail(
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin,
#     mixins.RetrieveModelMixin,
#     generics.GenericAPIView
# ):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
    
#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    