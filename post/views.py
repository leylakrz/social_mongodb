from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from post.queries.comment_queries import list_comment, create_comment
from post.queries.like_queries import list_like, create_like
from post.queries.post_queries import list_post, create_post, retrieve_post, check_post_exists


class PostApiView(APIView):
    def get(self, request, user_name):
        last_shown_id = request.GET.get("last_shown_id")
        return Response(list_post(last_show_id=last_shown_id, user_name=user_name))


class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        last_shown_id = request.GET.get("last_shown_id")
        return Response(list_post(last_show_id=last_shown_id))

    def create(self, request):
        return Response(create_post(user_name=request.user, text=request.data.get("text")))

    def retrieve(self, request, pk):
        obj = retrieve_post(obj_id=pk)
        if obj:
            return Response(obj)
        raise NotFound


class LikeViewSet(viewsets.ViewSet):
    lookup_field = "post_id"

    @action(detail=True, methods=["GET"], )
    def likes(self, request, post_id):
        last_shown_id = request.GET.get("last_shown_id")
        return Response(list_like(post_id=post_id, last_show_id=last_shown_id))

    @action(detail=True, methods=["POST"], )
    def like(self, request, post_id):
        if not check_post_exists(post_id, request.user):
            raise NotFound
        return Response()


class CommentViewSet(viewsets.ViewSet):
    lookup_field = "post_id"

    @action(detail=True, methods=["GET"], )
    def comments(self, request, post_id):
        last_shown_id = request.GET.get("last_shown_id")
        return Response(list_comment(post_id=post_id, last_show_id=last_shown_id))

    @action(detail=True, methods=["POST"], )
    def comment(self, request, post_id):
        if not check_post_exists(post_id):
            raise NotFound
        return Response(create_comment(user_name=request.user, post_id=post_id, text=request.data.get("text")))
