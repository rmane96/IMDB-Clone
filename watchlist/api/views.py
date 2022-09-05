from xml.dom import ValidationErr
import watchlist
from watchlist.api.serailizers import ReviewSerializer, WatchListSerializer, StreamPlatformSerializer
from rest_framework.response import Response
from rest_framework import status
from watchlist.models import StreamPlatform, WatchList, Review
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from watchlist.api.permissions import IsAdminOrReadOnly, ReviewOwnerOrReadOnly
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from watchlist.api.throttling import ReviewCreateThrottle, ReviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from watchlist.api.pagination import WatchListPagination



class ReviewList(generics.ListCreateAPIView):
    # throttle_classes = [ReviewCreateThrottle]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']
    
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(pk=pk)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    permission_classes = [ReviewOwnerOrReadOnly] 

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [ReviewOwnerOrReadOnly]
    
class ReviewCreate(generics.CreateAPIView):

    
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer
    
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        movie = WatchList.objects.get(pk=pk)
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie, review_user=review_user)
    
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this Movie')    
        if movie.number_rating == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating'])/2
        
        movie.number_rating =  movie.number_rating + 1        
        movie.save()
        serializer.save(watchlist=movie, review_user=review_user)
                 
class StreamPlatformRV(viewsets.ModelViewSet):
    
    permission_classes = [IsAdminOrReadOnly] 

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
class WatchListAV(generics.ListCreateAPIView):
    serializer_class = WatchListSerializer
    permission_classes = [IsAdminOrReadOnly] 
    queryset = WatchList.objects.all()
    
    
    
    
class MovieDetailsAV(APIView):
    permission_classes = [IsAdminOrReadOnly] 
    
    def get(self,request,pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie,context={'request': request})
            return Response(serializer.data)
        except WatchList.DoesNotExist:    
            return Response({'Error':'Movie not found'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self,request,pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    
    #directly mapping the parameter
    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(review_user__username=username)
    



        
# class ReviewList(mixins.ListModelMixin,
#                 mixins.CreateModelMixin,
#                 generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self,request,*args,**kwargs):
#         return self.create(request, *args, **kwargs)
    

# class ReviewDetail(mixins.ListModelMixin,
#                    mixins.CreateModelMixin,
#                    generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self,request,*args,**kwargs):
#         return self.list(request, *args, **kwargs)


# class StreamPlatformRV(viewsets.ViewSet):
    
#     def list(self,request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
        
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
    
#     def create(self,request):
#         serializer =  StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        


# class StreamPlatformAV(APIView):
#     def get(self,request):
#         platform = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platform, many= True, context={'request':request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer =  StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
# class StreamPlatformDetailAV(APIView):

#     def get(self, request, pk):
#         try:
#             platform = StreamPlatform.objects.get(pk=pk)
#         except StreamPlatform.DoesNotExist:
#             return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = StreamPlatformSerializer(platform,many=True,context={'request':request})
#         return Response(serializer.data)

#     def put(self, request, pk):
#         platform = StreamPlatform.objects.get(pk=pk)
#         serializer = StreamPlatformSerializer(platform, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         platform = WatchList.objects.get(pk=pk)
#         platform.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)