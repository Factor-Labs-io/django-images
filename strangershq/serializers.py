from rest_framework import serializers

class AddUserSerializer(serializers.Serializer):
    address = serializers.CharField()
    twitter_id = serializers.CharField()
    token_id = serializers.CharField()
    twitter_url = serializers.CharField()
    hometown = serializers.CharField()
    disc_handle = serializers.CharField()
    interests = serializers.CharField()

    def create(self, validated_data):
        # Perform any additional processing if needed
        return validated_data
    
class ReturnUserSerializer(serializers.Serializer):
    address = serializers.CharField()

    def create(self, validated_data):
        # Perform any additional processing if needed
        return validated_data

class UpdateHometownSerializer(serializers.Serializer):
    address = serializers.CharField()
    hometown = serializers.CharField()

    def create(self, validated_data):
        # Perform any additional processing if needed
        return validated_data
    
class UpdateInterestsSerializer(serializers.Serializer):
    address = serializers.CharField()
    interests = serializers.CharField()

    def create(self, validated_data):
        # Perform any additional processing if needed
        return validated_data
    
class TwitterTrackingSerializer(serializers.Serializer):
    token_id = serializers.CharField()
    handle = serializers.CharField()

    def create(self, validated_data):
        # Perform any additional processing if needed
        return validated_data
    
class LeaderboardSerializer(serializers.Serializer):

    def create(self):
        # Perform any additional processing if needed
        return self
    
    

