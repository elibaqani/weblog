from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from . import serializers
from .models import Blog, Comment
from .serializers import BlogSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self,request):
        try:
            blogs= Blog.objects.all().order_by('?')
            if request.GET.get('search'):
                search=request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search)| Q(content__icontains=search))


            page_number = request.GET.get('page',1)
            pagiantor =Paginator(blogs,3)
            serializer = BlogSerializer(pagiantor.page(page_number), many=True)

            return Response({
                "data": serializer.data,
                "message": "blogs fetched successfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
          print(e)
          return Response({
              "data":{},
              "message":"something went wrong",
          },status=status.HTTP_400_BAD_REQUEST)


    def post(self,request):
        try:
            data=request.data

            data['user'] =request.user.id

            serializer=BlogSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    "data": {},
                    "message": "someting went wrong"
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                "data": serializer.data,
                "message": "blog created successfully"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
          print(e)
          return Response({
              "data":{},
              "message":"something went wrong",
          },status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request):
        try:
            data= request.data
            blog=Blog.objects.filter(title=data.get("title"))
            print(blog[0].author)
            print(request.user)
            if not blog.exists():
                return Response({
                    "data": {},
                    "message": "invalid blog title"
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    "data": {},
                    "message": "you are not authorized to this"
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer = BlogSerializer(blog[0],data=data,many=True)
            if not serializer.is_valid():
                return Response({
                    "data": {},
                    "message": "someting went wrong"
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                "data": serializer.errors,
                "message": "your acount is created"
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                "data": {},
                "message": "something went wrong",
            }, status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get("id"))
            if not blog.exists():
                return Response({
                    "data": {},
                    "message": "invalid blog id"
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog[0].user:
                return Response({
                    "data": {},
                    "message": "you are not authorized to this"
                }, status=status.HTTP_400_BAD_REQUEST)

            blog[0].delete()
            return Response({
                "data": {},
                "message": "blog deleted"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                "data": {},
                "message": "something went wrong",
            }, status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(is_deleted=False)
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response({
            'data': serializer.data,
            'message': 'Comment created successfully',
            'status': status.HTTP_201_CREATED
        })

    def put(self, request, pk=None):
        comment = self.get_object()
        if comment.author != request.user:
            return Response({
                'message': 'You are not authorized to update this comment',
                'status': status.HTTP_403_FORBIDDEN
            })
        serializer = self.get_serializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({
            'data': serializer.data,
            'message': 'Comment updated successfully',
            'status': status.HTTP_200_OK
        })

    def delete(self, request, pk=None):
        comment = self.get_object()
        if comment.author != request.user and comment.blog_post.author != request.user:
            return Response({
                'message': 'You are not authorized to delete this comment',
                'status': status.HTTP_403_FORBIDDEN
            })
        comment.is_deleted = True
        comment.save()
        return Response({
            'message': 'Comment deleted successfully',
            'status': status.HTTP_204_NO_CONTENT
        })