from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from . models import Tweet
from users.models import User
from . serializers import TweetSerializer
from . permissions import IsOwnerOrReadOnly


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def liked(request, pk):

    tweet = Tweet.objects.get(pk=pk)

    if request.user in tweet.liked.all():
        print("user already liked this tweet")
        liked = False
        tweet.liked.remove(request.user)
    else:
        print("user liked this tweet")
        liked = True
        tweet.liked.add(request.user)
    return Response({
        'liked': liked,
        'count': tweet.likes_count
    })


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def like(request):
    if request.method == "POST":
        pk = request.data.get("pk")
        tweet = get_object_or_404(Tweet, id=pk)

        if request.user in tweet.liked.all():
            liked = False
            tweet.liked.remove(request.user)
        else:
            liked = True
            tweet.liked.add(request.user)
        return Response({
            'liked': liked,
            'count': tweet.like_count
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_tweets(request, username):
    user = User.objects.get(username=username)
    tweets = Tweet.objects.filter(user=user)
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)

class TweetList(generics.ListCreateAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer

    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]



