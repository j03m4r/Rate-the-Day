from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from datetime import date

##### AUTHENTICATION VIEWS #####
class CheckAuthenticated(APIView):
    def get(self, request, format=None):
        user = self.request.user
        is_authenticated = user.is_authenticated
        if is_authenticated:
            return Response({'Success': 'User is authenticated...', 'isAuthenticated': True}, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'User is not authenticated...', 'isAuthenticated': False}, status=status.HTTP_401_UNAUTHORIZED)
   
@method_decorator(csrf_protect, name='dispatch')
class SignUp(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        data = self.request.data
        
        username = data['username']
        password = data['password']
        re_password = data['re_password']
        
        if password == re_password:
            if User.objects.filter(username=username).exists():
                return Response({'Error': 'Username already exists...'}, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                user = User.objects.create_user(username=username, password=password)
                user = User.objects.get(id=user.id)
                
                UserProfile.objects.create(user=user, first_name='', last_name='', bio='')
                return Response({'Success': 'User created successfully...'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Passwords do not match...'}, status=status.HTTP_400_BAD_REQUEST)
        
@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        return Response({'Success': 'CSRF cookie set...'}, status=status.HTTP_200_OK)
    
@method_decorator(csrf_protect, name='dispatch')
class Login(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request, format=None):
        data = self.request.data
        
        username = data['username']
        password = data['password']
        
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return Response({'Success': 'Logged in successfully...'}, status=status.HTTP_200_OK)
        else:
            return Response({'Error': 'Could not log in...'}, status=status.HTTP_400_BAD_REQUEST)
        
class Logout(APIView):
    def post(self, request, format=None):
        auth.logout(request)
        return Response({'Success': 'Logged out successfully...'}, status=status.HTTP_200_OK)
    
class Delete(APIView):
    def delete(self, request, format=None):
        try:
            user = self.request.user
            user = User.objects.filter(id=user.id)
            user.delete()
            return Response({'Success': 'User deleted successfully'}, status=status.HTTP_200_OK)
        except:
            return Response({'Error': 'Something went wrong deleting user'}, status=status.HTTP_400_BAD_REQUEST)
        
class GetUsers(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def get(self, request, format=None):
        users = User.objects.all()
        
        users = UserSerializer(users, many=True)
        return Response({'users': users.data}, status=status.HTTP_200_OK)
    
##### PROFILE VIEWS #####
class GetProfile(APIView):
    def get(self, request, format=None):
        user = self.request.user
        username = user.username
        
        profile = UserProfile.objects.get(user=user)
        profile = ProfileSerializer(profile)
        
        return Response({ 'profile': profile.data, 'username': str(username)}, status=status.HTTP_200_OK)
    
class GetOtherProfile(APIView):
    lookup_url_kwarg = "username"
    
    def get(self, request, format=None):
        username = request.GET.get(self.lookup_url_kwarg)
        if username != None:
            user = User.objects.filter(username=username)[0]
            profile = UserProfile.objects.filter(user=user)[0]
            profile = ProfileSerializer(profile)
            return Response({ 'profile': profile.data, 'username': str(username)}, status=status.HTTP_200_OK)
        return Response({ 'Error': 'Could not find user...' }, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateProfile(APIView):
    def patch(self, request, format=None):
        user = self.request.user
        username = user.username
        
        profile = UserProfile.objects.filter(user=user)[0]
        
        data = self.request.data
        first_name = data['first_name']
        last_name = data['last_name']
        bio = data['bio']
        
        profile.first_name = first_name
        profile.last_name = last_name
        profile.bio = bio
        profile.save(update_fields=['first_name', 'last_name', 'bio'])
        profile = ProfileSerializer(profile)
        
        return Response({ 'profile': profile.data, 'username': str(username) }, status=status.HTTP_200_OK)

class Rate(APIView):
    def post(self, request, format=None):
        data = self.request.data
        user = self.request.user
        profile = UserProfile.objects.filter(user=user)[0]
        
        rating = data['rating']
        description = data['description']
        dayRating = DayRating(user=user, rating=rating, description=description)
        dayRating.save()
        
        profile.ratings.add(dayRating)
        
        return Response({'Success': 'Rating successfully created...'}, status=status.HTTP_201_CREATED)

class Follow(APIView):
    def post(self, request, format=None):
        data = self.request.data
        otherUser = User.objects.filter(username=data['username'])[0]
        user = self.request.user
        
        profile = UserProfile.objects.filter(user=user)[0]
        otherProfile = UserProfile.objects.filter(user=otherUser)[0]
        
        profile.following.add(otherUser)
        otherProfile.followers.add(user)

        profile = ProfileSerializer(profile)
        otherProfile = ProfileSerializer(otherProfile)
        
        return Response({'Success': 'Followers and following successfully updated...', 'profile': profile.data, 'otherProfile': otherProfile.data }, status=status.HTTP_200_OK)

class Unfollow(APIView):
    def post(self, request, format=None):
        data = self.request.data
        other_user = User.objects.filter(username=data['username'])[0]
        other_profile = UserProfile.objects.filter(user=other_user)[0]
        
        user = self.request.user
        profile = UserProfile.objects.filter(user=user)[0]
        
        profile.following.remove(other_user)
        other_profile.followers.remove(user)

        profile = ProfileSerializer(profile)
        other_profile = ProfileSerializer(other_profile)
        
        return Response({'Success': 'Followers and following successfully updated...', 'profile': profile.data, 'otherProfile': other_profile.data}, status=status.HTTP_200_OK)
    
class GetRating(APIView):
    lookup_url_kwarg = "id"
    
    def get(self, request, format=None):
        id = request.GET.get(self.lookup_url_kwarg)
        
        if id != None:
            rating = DayRating.objects.filter(id=id)
            if rating.exists():
                rating = rating[0]
                profile = rating.profile.all()[0]
                username = profile.user.username
                rating = RatingSerializer(rating)
                return Response({'Success': 'Rating successfully returned...', 'rating': rating.data, 'username': username}, status=status.HTTP_200_OK)
            return Response({'Error': 'Rating could not be found...'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Error': 'No id provided...'}, status=status.HTTP_400_BAD_REQUEST)

class GetFollowingRatings(APIView):
    def get(self, request, format=None):
        user = self.request.user
        profile = UserProfile.objects.filter(user=user)[0]
        following = profile.following.all()
        currentDate = date.today()
        
        ratings = DayRating.objects.filter(date=currentDate, profile__user__in=following)
        local_rating = DayRating.objects.filter(profile__user=user, date=currentDate)
        if local_rating!=None:
            ratings = ratings | local_rating
            
        ratings = RatingSerializer(ratings, many=True)
        
        return Response({'Success': 'Ratings successfully returned...', 'ratings': ratings.data}, status=status.HTTP_200_OK)

class LikeRating(APIView):
    def post(self, request, format=None):
        data = self.request.data
        id = data['id']

        if id !=None:
            user = self.request.user
            
            rating = DayRating.objects.get(id=id)
            rating.likes.add(user)
            rating = RatingSerializer(rating)
            
            return Response({'Success': 'Successfully liked...', 'rating': rating.data}, status=status.HTTP_201_CREATED)
        return Response({'Error': 'No id provided...'}, status=status.HTTP_400_BAD_REQUEST)

class MakeComment(APIView):
    def post(self, request, format=None):
        user = self.request.user
        data = self.request.data
        id = data['id']
        
        content = data['content']
        comment = Comment(user=user, text=content)
        comment.save()
        
        rating = DayRating.objects.get(id=id)
        rating.comments.add(comment)
        rating = RatingSerializer(rating)
        
        return Response({'Success': 'Successfully liked...', 'rating': rating.data}, status=status.HTTP_201_CREATED) 
        