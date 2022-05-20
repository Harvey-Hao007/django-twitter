from rest_framework import viewsets
from tweets.models import Tweet
from tweets.api.sertializers import TweetCreateSerializer, TweetSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response


class TweetViewSet(viewsets.GenericViewSet,
                   viewsets.mixins.CreateModelMixin,
                   viewsets.mixins.ListModelMixin):
    """
    API endpoint that allows users to create, list tweets
    """
    queryset = Tweet.objects.all()
    serializer_class = TweetCreateSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        """
        overload create method, because we need to set current user as tweet.user
        """
        serializer = TweetCreateSerializer(
            data=request.data,
            context={'request': request},
        )

        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': "Please check input",
                'errors': serializer.errors,
            }, status=400)
        tweet = serializer.save()
        return Response(TweetSerializer(tweet).data, status=201)

    def list(self, request, *args, **kwargs):
        """
        overload list method, not list all tweets instead must
        require user_id as filter
        """
        if 'user_id' not in request.query_params:
            return Response('missing user_id', status=400)

        tweets = Tweet.objects.filter(
            user_id=request.query_params['user_id']
        ).order_by('-created_at')
        serializer = TweetSerializer(tweets, many=True)
        return Response({'tweets': serializer.data})

