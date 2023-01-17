from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, DayRating, Comment
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = UserSerializer(read_only=True, many=True)
    
    class Meta:
        model = DayRating
        fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(read_only=True, many=True)
    following = UserSerializer(read_only=True, many=True)
    followers = UserSerializer(read_only=True, many=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'