from django.http import JsonResponse

from rest_framework.decorators import api_view

from account.models import User
from account.serializers import UserSerializer

from .models import Post, Like

from .serializers import PostSerializer

from .forms import PostForm


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]
    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
def post_list_profile(request, id):
    user = User.objects.get(pk=id)
    user_serializer = UserSerializer(user)

    posts = Post.objects.filter(created_by=user)
    post_serializer = PostSerializer(posts, many=True)

    return JsonResponse({
        'user': user_serializer.data,
        'posts': post_serializer.data,
    }, safe=False)


@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        serializer = PostSerializer(post)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'post not created'})


@api_view(['POST'])
def post_like(request, id):
    post = Post.objects.get(id=id)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)
        post.like_count += 1
        post.likes.add(like)
        post.save()

        message = 'like created'
    else:
        message = 'already liked'

    return JsonResponse({'message': message})
