from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.authentication import generate_access_token
from user_profile.queries import check_user_name_exists, create_user


class Login(APIView):
    authentication_classes = []

    def post(self, request, ):
        user_name = request.data.get("user_name")
        if not check_user_name_exists(user_name):
            create_user(user_name)

        return Response(data={"user_name": user_name,
                              "access_token": generate_access_token(user_name)})
