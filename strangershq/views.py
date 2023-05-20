from django.shortcuts import render
from rest_framework.response import Response 
from rest_framework import status
from . import database, pfp_tracking
from rest_framework.views import APIView
from .serializers import AddUserSerializer, ReturnUserSerializer, UpdateHometownSerializer, UpdateInterestsSerializer, TwitterTrackingSerializer

from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')

class AddUserView(APIView):
    def post(self, request):
        serializer = AddUserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            handle = validated_data['handle']
            token = validated_data['token']
            twitter_url = validated_data['twitter_url']
            hometown = validated_data['hometown']
            disc_handle = validated_data['disc_handle']
            interests = validated_data['interests']
            print("---------")
            print(validated_data)
            print("---------")
            # Perform further processing with the data
            result = database.dbAddUser(address, handle, token, twitter_url, hometown, disc_handle, interests)
            pfp_status = pfp_tracking.pfpCompare(token, handle)
            if pfp_status[0] == True:
                database.dbUpdatePFP(token)
            if pfp_status[0] == False:
                database.dbUpdatePFPFalse(token)
            return Response({'message': 'User added successfully\n'}, result)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ReturnUserView(APIView):
    def post(self, request):
        serializer = ReturnUserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            result = database.dbQueryRow(address)
            print(result)
            return Response({'message': f'{result}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteUserView(APIView):
    def post(self, request):
        serializer = ReturnUserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            result = database.dbDeleteRow(address)
            if result['status'] == 'Success':
                return Response({'message': f'{address} deleted successfully'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UpdateUserHometownView(APIView):
    def post(self, request):
        serializer = UpdateHometownSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            hometown = validated_data['hometown']
            result = database.dbUpdateHometown(address, hometown)
            if result['status'] == 'Success':
                return Response({'message': f'{address} successfully changed hometown to: {hometown}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserInterestsView(APIView):
    def post(self, request):
        serializer = UpdateInterestsSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            address = validated_data['address']
            interests = validated_data['interests']
            result = database.dbUpdateInterests(address, interests)
            if result['status'] == 'Success':
                return Response({'message': f'{address} successfully changed interests to: {interests}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def fetch_leaderboard():
    result = database.dbQueryLeaderBoard()
    return JsonResponse({'message': f'{result}'})

class TwitterTrackingView(APIView):
    def post(self, request):
        serializer = TwitterTrackingSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # Process the validated data
            token = validated_data['token']
            handle = validated_data['handle']
            result = pfp_tracking.twitterTracking(token, handle)
            return Response({'message': f'{result}'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# def twitter_tracking(request):
#     result = pfp_tracking.twitterTracking(request)
#     return JsonResponse({'message': 'Twitter tracking performed successfully'})

