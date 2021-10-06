from typing import Counter
from django import views
from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import activate
from django.views import View
from django.contrib import messages
from .models import Following, Notification, Person, Post, Liked, Comment
from datetime import datetime

from .forms import Signupform, LoginForm
# Create your views here.
#to send notifications
def send_notification(sender, receiver, message):
    if sender!=receiver:
        Notification(sender_id=sender, receiver_id=receiver, message = message, time=datetime.now()).save()


def index(request):
    return render(request, 'index.html')

class Signup(View):
    def get(self, request):
        if not request.user.is_authenticated:
            fm = Signupform()
            return render(request, 'signup.html',{'form':fm})
        else:
            return redirect('/home/')    
    def post(self, request):
        fm = Signupform(request.POST)
        if fm.is_valid():
            fm.save()
               
            user = authenticate(username = fm.cleaned_data['username'], password = fm.cleaned_data['password1'])
            login(request, user)
            messages.success(request,'User Account Created Successfully, Welcome to your home page!') 
            return redirect('/home/')
        else:
            messages.error(request, "Failed to create User")    
        return render(request, 'signup.html',{'form':fm})

class Login(View):
    def get(self, request):
        if not request.user.is_authenticated:
            fm = LoginForm()
            return render(request, 'login.html',{'form':fm}) 
        else:
            return redirect('/home/') 

    def post(self, request):
        fm = LoginForm(request= request, data = request.POST)
        username = request.POST['username']    
        password = request.POST['password'] 
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success( request, 'Succcessfully logged in !')
            return redirect('/home/')
        else:
            messages.error(request, "Invalid credentials!") 
            return render(request, 'login.html',{'form':fm}) 


def get_following_persons(person_id):
    following_persons = set()
    following = Following.objects.filter(follower = person_id)
    for cbs in following:
        following_persons.add(cbs.following)
    return following_persons    

def getUserLikeStatus(person_id, post_id):
    count = Liked.objects.filter(person_id = person_id, post_id=post_id, liked = 1).count()
    if count>0:
        return True
    else:
        return False  

def getCommentCount(postid):
    return Comment.objects.filter(post_id = postid).count()

class Home(View):   
    def get(self, request):
        
        if request.user.is_authenticated: 
            
            person = Person.objects.get(pk = request.user.id)
            following = Following.objects.filter(follower = person.id)
            following_list = set()
            for cbs in following:
                following_list.add(cbs.following_id)
                
            following_list.add(person.id)

            following_persons = get_following_persons(person.id)
            
            posts = Post.objects.filter(person_id__in = following_list).order_by('-time')

            post_modified=[]
            #modify posts in queryset
            for post in posts:
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
                        'user_liked': getUserLikeStatus(person.id, post.id),
                        'comment_count':getCommentCount(post.id),
                    }
                ) 
                  
            recent_members = Person.objects.all().order_by('-followers')[:10]
            count_new_notifications = Notification.objects.filter(receiver_id = person.id, read = False).count()
            contents = {
                'posts':post_modified,
                'active':person,
                'others': recent_members,
                'following_list':following_list,
                'following_persons': following_persons,
                'count_n' : count_new_notifications,
                'homepage':True,
            }
            return render(request, 'home.html', contents)
        else:
            return redirect('/login/')  
    def post(self, request):
        user = request.user
        type = request.POST['type-of-file']
        if type=="video":
            print("Video Upload")
            time = datetime.now()
            videofile = request.FILES['videofile']
            desc = request.POST['desc']
            print(time, desc, videofile)

            post = Post(person_id = request.user.id, time=time, type=type, video = videofile, desc = desc)
            post.save()

        elif type == "image":
            print("Image Upload")
            time = datetime.now()
            imagefile = request.FILES['imagefile']
            desc = request.POST['desc']
            print(time, imagefile, desc)

            post = Post(person_id = request.user.id, time=time, type=type, image = imagefile, desc = desc)
            post.save()
        else:
            print("Text Upload")
            time = datetime.now()
            text = request.POST['textdata']
            desc = request.POST['desc']
            print(time, text, desc)

            post = Post(person_id = request.user.id, time=time, type=type, text = text, desc = desc)
            post.save()
        messages.success(request,"Your post was successfully upploaded !")
        return redirect('/home/')    


def logout_user(request):
    
    # messages.success( request, 'Succcessfully logged out !')
    logout(request)
    return redirect("/")

#like-dislike-----------------------------------------------------------------
def like_post(request):
    post_id = int(request.GET['postid'])
    person_id = request.user.id
    noc = Liked.objects.filter(post_id = post_id, person_id = person_id).update(liked = 1)
    if noc == 0:
        liked = Liked(post_id = post_id, person_id = person_id, liked = 1)
        liked.save()
    Post.objects.filter(id = post_id).update(likes = Post.objects.get(pk = post_id).likes + 1 ) 

    #sending notification
    receiver_id = Post.objects.get(pk = post_id).person_id
    send_notification(person_id, receiver_id, "liked your post.")

    return JsonResponse({'success':'liked'})

def remove_like(request):
    post_id = int(request.GET['postid'])
    person_id = request.user.id

    noc = Liked.objects.filter(post_id = post_id, person_id = person_id).update(liked = 0)
    
    Post.objects.filter(id = post_id).update(likes = Post.objects.get(pk = post_id).likes - 1 ) 
    
    return JsonResponse({'success':'removed_like'}) 

def profile(request, personid):
    # print(personid, type(personid))

    person = Person.objects.get(pk = personid)
    active = Person.objects.get(pk = request.user)
    posts = Post.objects.filter(person_id = personid).order_by('-time')
    count_posts = posts.count()

    post_modified=[]
    #modify posts in queryset
    for post in posts:
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
                'user_liked': getUserLikeStatus(active.id, post.id),
                'comment_count':getCommentCount(post.id),
            }
        )    

    contents = {
        'posts':post_modified,
        'person':person,
        'active':active,
        'following_persons': get_following_persons(active.id),
        'count_posts': count_posts,
    }

    return render(request, 'profile.html', contents)

#updates --------------------------------------------------------

def pic_update(request):
    personid = request.user.id
    try:
        file = request.FILES['update-field']
        person = Person.objects.get(pk=personid)
        person.pic = file
        person.save()

        messages.success(request, 'successfully updated Profile Pic')
        print(file)
    except Exception:
        Person.objects.filter(id = personid).update(pic = None)
        messages.success(request, 'successfully removed Profile Pic')

    print('pic update')
    return redirect(f'/profilepage/{personid}')
def bgpic_update(request):
    personid = request.user.id
    try:
        file = request.FILES['update-field']
        person = Person.objects.get(pk=personid)
        person.bgpic = file
        person.save()

        messages.success(request, 'successfully updates Cover Photo')
        print(file)
    except Exception:
        Person.objects.filter(id = personid).update(bgpic = None)
        messages.success(request, 'successfully removed Cover Photo')
    print('bgpic update')
    return redirect(f'/profilepage/{request.user.id}')

def pro_update(request):
    personid = request.user.id
    try:
        data = request.POST['update-field']
        Person.objects.filter(id = personid).update(profession = data)

        messages.success(request, 'successfully updated Profession')
    except Exception:
        Person.objects.filter(id = personid).update(profession = None)
        messages.success(request, 'successfully removed Profession')

    return redirect(f'/profilepage/{request.user.id}')

def bio_update(request):
    personid = request.user.id
    try:
        data = request.POST['update-field']
        Person.objects.filter(id = personid).update(bio = data)

        messages.success(request, 'successfully updated Bio')
    except Exception:
        Person.objects.filter(id = personid).update(bio = None)
        messages.success(request, 'successfully removed Bio')

    return redirect(f'/profilepage/{request.user.id}')

def cc_update(request):
    personid = request.user.id
    try:
        data1 = request.POST['update-field-city']
        data2 = request.POST['update-field-country']
        Person.objects.filter(id = personid).update(city = data1, country = data2)

        messages.success(request, 'successfully updated location')
    except Exception:
        Person.objects.filter(id = personid).update(city = None, country = None)
        messages.success(request, 'successfully removed location')

    return redirect(f'/profilepage/{request.user.id}')


# comments

def showComments(request):
    post_id = int(request.GET['postid'])
    relevant_comments = Comment.objects.filter(post_id = post_id).order_by('-time')
    final_list =[]
    for ct in relevant_comments:
        final_list.append(
            {
                'name': ct.person.first_name +" "+ ct.person.last_name,
                'comment': ct.comment,
            }
        )   
    return JsonResponse(final_list, safe=False)    



def addComment(request):
    post_id = int(request.GET['postid'])
    person_id = request.user.id
    comment_data = request.GET['commentdata']
    time = datetime.now()
    new_comment = Comment(post_id = post_id, person_id=person_id, comment = comment_data, time = time)
    new_comment.save()

    #sending notification
    receiver_id = Post.objects.get(pk = post_id).person_id
    send_notification(person_id, receiver_id, "commented on your post.")

    return JsonResponse(
        {'success':'comment saved'}
    )    

#-----------follow-unfollow--------------------
def follow(request):
    
    follower = request.user.id
    following = int(request.GET['id'])

    Following(follower_id=follower, following_id=following).save()

    #update no_of_followers
    count_of_followers = Following.objects.filter(following_id=following).count()
    Person.objects.filter(id = following).update(followers = count_of_followers)
    
    #sending notification

    send_notification(follower, following, "started following you.")

    return JsonResponse(
        {'following': 'added' }
    )


def unfollow(request):
    
    follower = request.user.id
    following = int(request.GET['id'])

    Following.objects.filter(follower_id=follower, following_id=following).delete()

    #update no_of_followers
    count_of_followers = Following.objects.filter(following_id=following).count()
    Person.objects.filter(id = following).update(followers = count_of_followers)
    
    return JsonResponse(
        {'following': 'removed' }
    )
