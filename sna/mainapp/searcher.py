from typing import Counter
from django import views
from django.contrib.auth import authenticate, login, logout
from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import activate
from django.views import View
from django.contrib import messages
from .models import Following, Person, Post, Liked, Comment, Notification
from datetime import datetime, time
from django.db.models import Q, Subquery
from .views import getCommentCount, getUserLikeStatus

class Searcher(View):
    def get(self, request):
        return render(request, 'search.html')
    def post(self, request):
        search = request.POST['term']
        if search != "" and search!=" ":
             
            profiles = Person.objects.filter(Q(username__icontains = search) | Q(first_name__icontains = search)) 


            posts = Post.objects.filter(Q(desc__icontains = search) | Q(text__icontains = search)).order_by('-time')

            contents = {
                'profiles':profiles,
                'posts':posts,
            }   
            return render(request, 'search.html', contents)
        else:
            return render(request, 'search.html')    

def liked_page(request):
    active = Person.objects.get(pk = request.user.id)

    liked_details = Liked.objects.filter(person_id = active.id, liked = 1)
    liked_posts = Post.objects.filter(id__in = Subquery(liked_details.values('post_id'))).order_by('-time')

    post_modified=[]
    #modify posts in queryset
    for post in liked_posts:
        post_modified.append(
            {
                'id': post.id,
                'person' : post.person,
                'time' : post.time,
                'type' : post.type,
                'desc' : post.desc,
                'video' : post.video,
                'image' : post.image,
                'text' : post.text,
                'likes' : post.likes,
                'user_liked': True,
                'comment_count':getCommentCount(post.id),
            }
        )  

    context = {
        'active':active,
        'posts':post_modified, 
    }
    return render(request, 'liked.html',context=context)         

def delete_post(request, postid):
    Post.objects.filter(id = postid).delete()
    return redirect("/profilepage/"+str(request.user.id)+"/")

def notification_handler(request, activeid):

    if request.user.is_authenticated:
        notifications = Notification.objects.filter(receiver_id = activeid).order_by('-time')
        active = Person.objects.get(pk = activeid)

        context = {
            'notifications':notifications,
            'active':active,
            'homepage': True,
        }
        Notification.objects.filter(receiver_id = activeid).update(read = True)
        return render(request, 'notification.html', context=context)