from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.models import update_last_login
from django.http import Http404
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import NotFound


from .permissions import IsOwner,IsCustomer
from .serializers import CustomUserSerializer, CustomerInfo
from .models import CustomUser

class OwnerCrudOperations(APIView):
    #only onwer can register
    permission_classes = [IsOwner]

    #get all users(customers and owners)
    def get(self, request):
        try:
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #update user by considering token
    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#get all owners
@api_view(["GET"])
@permission_classes([IsOwner])
def get_owners(request):
    try:
        users = CustomUser.objects.filter(is_owner=True)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

#get all customers
@api_view(["GET"])
@permission_classes([IsOwner])
def get_customers(request):
    try:
        
        users = CustomUser.objects.filter(is_customer=True)
        if not users.exists():  
            return Response({"message": "No customers found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomUserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    



class ManageUserView(RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        """Override get_object to handle user not found scenario"""
        try:
            return super().get_object()
        except Http404:
            raise NotFound("User not found")



    #get specific user detail
    def get(self, request, *args, **kwargs):
        """Retrieve a specific user"""
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


    #update the user details
    def put(self, request, *args, **kwargs):
        """Update user details"""
        user = self.get_object()
        if not user.is_active:
            return Response({"message": "User is inactive and cannot be updated"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(user,data=request.data, partial=True)  # partial=True to allow updating only specific fields
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(["PATCH"])
@permission_classes([IsOwner])
def deactivate_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)

        # Check if the user is an owner and if deactivating would leave no active owners
        if user.is_owner:
            # Check if there is at least one other active owner
            active_owners_count = CustomUser.objects.filter(is_owner=True, is_active=True).exclude(pk=pk).count()
            
            if active_owners_count == 0:
                return Response({"message": "There must be at least one active owner."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_active:
            return Response({"message": "User is already deactivated"}, status=status.HTTP_400_BAD_REQUEST)

        # Deactivate the user
        user.is_active = False
        user.save()
        return Response({"message": "User has been deactivated"}, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(["PATCH"])
@permission_classes([IsOwner])
def activate_user(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)

        if user.is_active:
            return Response({"message": "User is already active"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({"message": "User has been activated"}, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)





#search the user with username or email
@api_view(["GET"])
@permission_classes([IsOwner])
def search_users(request):
    query = request.query_params.get('query', None)
    if not query:
        return Response({"message": "Please provide a search query"}, status=status.HTTP_400_BAD_REQUEST)

    # Get users that start with the query first
    starts_with = CustomUser.objects.filter(
        Q(username__istartswith=query) | Q(email__istartswith=query)
    ).order_by('username')  # Prioritize names that start with 'query'

    # Get users that contain the query (but do not start with it)
    contains = CustomUser.objects.filter(
        Q(username__icontains=query) | Q(email__icontains=query)
    ).exclude(id__in=starts_with).order_by('username')  # Remaining matches

    # Combine both querysets
    users = list(starts_with) + list(contains)

    if not users:
        return Response({"message": "No users found matching the search query"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class OwnerLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)  # Now it works with email

        if user:
            # Check if the user is an owner and active
            if user.is_owner and user.is_active:
                login(request, user)  # Log the user in
                token, created = Token.objects.get_or_create(user=user)  # Get or create token
                update_last_login(None, user)  # Update last login time
                return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'User is either not an owner or inactive'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)





#get all inactive users
@api_view(["GET"])
@permission_classes([IsOwner])
def get_inactive_users(request):
    try:
        users = CustomUser.objects.filter(is_active=False)
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    


class CustomerLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)  # Now it works with email

        if user:
            # Check if the user is an owner and active
            if user.is_customer and user.is_active:
                login(request, user)  # Log the user in
                token, created = Token.objects.get_or_create(user=user)  # Get or create token
                update_last_login(None, user)  # Update last login time
                return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
            elif not user.is_customer:
                return Response({'error': 'Only Customer can login'}, status=status.HTTP_401_UNAUTHORIZED)
            elif not user.is_active:
                return Response({'error': 'account deactivated'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'User is either not an owner or inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            
            
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


#customer can see profile, deactivate the profile
class CustomerProfile(APIView):
    permission_classes = [IsCustomer]
    def get(self, request):
        try:
            user = request.user
            serializer = CustomerInfo(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'error':'profile not found'},status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request):
        """Allow customers to update their profile"""
        user = request.user

        # Prevent updating if user is inactive
        if not user.is_active:
            return Response({"message": "User is inactive and cannot be updated"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomerInfo(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    #deactivate the profile by updating the active status into false
    def patch(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message':'profile deactivated'}, status=status.HTTP_200_OK)
   
        

