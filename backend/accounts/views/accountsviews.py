from rest_framework.views import APIView
from rest_framework import status
from accounts.models import User
from accounts.serializers import UsersSerializer
from django.http import Http404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class UsersAPI(APIView):
    """
    API View for retrieving the authenticated user's data.

    This view is accessible only by authenticated users and returns the data 
    for the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Endpoint to get the authenticated user's details.

        :param request: The HTTP request object.
        :return: JSON response with the user data and status 200 OK.
        """
        users = request.user
        serializer = UsersSerializer(users)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAPI(APIView):
    """
    API View for handling individual user operations (get, put, delete).

    This view is accessible only by authenticated users and allows them to 
    retrieve, update, or delete their own data.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, username):
        """
        Retrieve the user from the database by username.

        :param username: The username of the user to retrieve.
        :return: The user object if found.
        :raise Http404: If the user does not exist.
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, username):
        """
        Endpoint to get details of a user by their username.

        :param username: The username of the user whose data is to be retrieved.
        :return: JSON response with user data and status 200 OK.
        :raises Http404: If the user does not exist.
        """
        if request.user.username != username:
            return Response({"detail": "You do not have permission to access this user's data."},
                            status=status.HTTP_403_FORBIDDEN)

        user = self.get_object(username=username)
        serializer = UsersSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        """
        Endpoint to update a user's data.

        :param username: The username of the user whose data is to be updated.
        :return: JSON response with updated user data and status 202 ACCEPTED if successful.
        :raises Http404: If the user does not exist.
        :raises ValidationError: If the data provided is invalid.
        """
        if request.user.username != username:
            return Response({"detail": "You do not have permission to update this user's data."},
                            status=status.HTTP_403_FORBIDDEN)

        user = self.get_object(username=username)
        serializer = UsersSerializer(user, data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, username):
        """
        Endpoint to delete a user's account.

        :param username: The username of the user to delete.
        :return: Response with status 204 NO CONTENT if successful.
        :raises Http404: If the user does not exist.
        """
        if request.user.username != username:
            return Response({"detail": "You do not have permission to delete this user's account."},
                            status=status.HTTP_403_FORBIDDEN)

        user = self.get_object(username=username)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCreateAPI(APIView):
    """
    API View for creating a new user.

    This view does not require authentication and allows the creation of a new user.
    """
    permission_classes = []

    def post(self, request):
        """
        Endpoint to create a new user.

        :param request: The HTTP request object containing user data.
        :return: JSON response with the created user data and status 201 CREATED if successful.
        :raises ValidationError: If the provided data is invalid.
        """
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
