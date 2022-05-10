from dataclasses import fields
from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.contrib import messages

from .models import musictrack, playlist
from .forms import QuestionForm, SearchForm, ReviewForm, ReviewEditForm

from accounts.models import GUprofile
from .models import musictrack, music_reviews

from django.template.loader import render_to_string
from django.http import JsonResponse

import json
from django.core import serializers
from django.core.paginator import Paginator

from django.conf import settings

#-------------------------------------------------------------------------------
# search bar included list
def musiclist(request):
    tracks = None
    newtracks =  None
    ratedtracks = None
    form = SearchForm
    searched = False

    newtracks = musictrack.objects.all().order_by('-uploaded_date')[0:12]
    ratedtracks = musictrack.objects.all().order_by('likes_count')[0:12] 

    print(newtracks)
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            searchkey = form.cleaned_data['searchkey']
            print(searchkey)
            tracks = musictrack.objects.filter(Q(track_name__icontains=searchkey)|Q(track_creator__icontains=searchkey))
            #tracks2 = musictrack.objects.filter(track_name__icontains=searchkey)|musictrack.objects.filter(track_creator__icontains=searchkey)
            print(tracks)
            searched = True
            context = {"searched":searched,"tracks":tracks,"form":form}
            return render(request, 'musicplayer/music_list.html',context)

    context = {"searched":searched,"tracks":tracks,"newtracks":newtracks,"ratedtracks":ratedtracks,"form":form}
    return render(request, 'musicplayer/music_list.html',context)

#-----------question to find the mood
def questions(request):
    form = QuestionForm
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            answer1 = form.cleaned_data['question1']
            print(answer1)
            tempprofile = request.user.guprofile
            tempprofile.current_mood = answer1 
            tempprofile.save()
            print("updated")
            return redirect('musiclist')
    context = {"form":form}
    return render(request, 'musicplayer/music_questions.html',context)


#-----------music info of the selected music track
def music_info(request,pk):
    trackinfo = musictrack.objects.get(id=pk)
    liked = False
    if trackinfo.likes.filter(id=request.user.id).exists():
        liked=True;

    context = {"track":trackinfo, "liked":liked}
    return render(request, 'musicplayer/music_info.html',context)


#-----------music like of the selected music track  ajax
def music_like(request):
    if request.POST.get('action')=="post":
        result=''
        liked = False
        id = int(request.POST.get('postid'))
        post = get_object_or_404(musictrack, id=id)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.likes_count -= 1
            result = post.likes_count
            print(result)
            post.save()
            liked=False
        else:
            post.likes.add(request.user)
            post.likes_count += 1
            result = post.likes_count
            post.save()
            liked=True
            print(result)
        print("like now")
        return JsonResponse({'result':result,'liked':liked,})

    print("like now")
    return render(request, 'musicplayer/music_info.html')



#-----------Music review of the selected music track
def reviews_list(request,pk):
    trackinfo = musictrack.objects.get(id=pk)
    reviewlist = music_reviews.objects.filter(track_fk=pk)
    form = ReviewForm
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            reviewtext = form.cleaned_data['reviewtext']
            ruser = request.user
            rtrack = trackinfo
            print(reviewtext)
            newreview = music_reviews(review_text = reviewtext, reviewed_by = ruser, track_fk = rtrack)
            newreview.save()

            form=ReviewForm
            messages.success(request, "Successfully posted your review!")
            return redirect('reviews_list',pk)
            trackinfo = musictrack.objects.get(id=pk)
            reviewlist = music_reviews.objects.filter(track_fk=pk)
            context = {"track":trackinfo, "reviewlist":reviewlist,"form":form, "messages":messages}
            messages.success(request, "Successfully posted your review!")
            return render(request, 'musicplayer/music_review_list.html',context)
    print(reviewlist)
    context = {"track":trackinfo, "reviewlist":reviewlist,"form":form}
    return render(request, 'musicplayer/music_review_list.html',context)


#------------Delete music review of the selected music track
def delreview(request,pk):
    delrev = music_reviews.objects.get(id=pk)
    tid = delrev.track_fk.id
    print(tid)
    delrev.delete()
    messages.success(request, "Successfully deleted your review!")
    return redirect("reviews_list",tid)


#------------EDIT music review of the selected music track
def editreview(request,pk):
    editrev = music_reviews.objects.get(id=pk)
    tid = editrev.track_fk.id
    form = ReviewEditForm(instance = editrev)
    if request.method =='POST':
        form = ReviewEditForm(request.POST)
        if form.is_valid():
            editrev.review_text = form.cleaned_data['review_text']
            editrev.save()
            messages.success(request, "Successfully Edited your review!")
            return redirect("reviews_list",tid)
    context = {"form":form}
    return render(request, 'musicplayer/music_review_edit.html',context)



#------------list of available playlists
def playlist_list(request):
    cat = request.user.guprofile.current_mood
    try:
        rplist = playlist.objects.filter(category_fk = cat)
   
    except:
        rplist = None

    try:
        plist = playlist.objects.all()
   
    except:
        plist = None


    context = {"plist":plist, "rplist":rplist}
    return render(request, 'musicplayer/playlist_list.html',context)


#------------Delete music review of the selected music track
def playlistplayer(request,pk):
    try:
        plist = playlist.objects.get(id = pk)
   
    except:
        plist = None

    ptracks = plist.musictracks.all()

    def QuerysetToDict(obj):
        di = {}
        di["name"] = obj.track_name
        di["path"] =str(obj.track_path.url)
        di["image"] =str(obj.cover_image.url)
        return di

    clist = []

    for each in ptracks:
        d = QuerysetToDict(each)
        clist.append(d)

    jsonlist = json.dumps(clist)

    context = {'jsonlist':jsonlist}
    return render(request, 'musicplayer/playlist_player.html', context)


#----------MUSIC player method--------------lists the music tracks
def musicplayer(request):
    cat = request.user.guprofile.current_mood
    tplaylist = playlist.objects.get(category_fk = cat)
    print(tplaylist)

    curplaylist = tplaylist.musictracks.all()
    print("curr playlist")

    print(settings.MEDIA_ROOT.replace('\\','/'))
    tpath = settings.MEDIA_ROOT.replace('\\','/')
    mpath = tpath.replace('MEDIA','media')

    cplist = list(curplaylist.values())
    #print(cplist)
    jsonlist = serializers.serialize("json", tplaylist.musictracks.all(), fields=('track_name','track_path'))
    #jsonlist = json.dumps(jsonlist)

    mpath = "http:://127.0.0.1:8000/MEDIA"
    def qtod(obj):
        di = {}
        di["name"] = obj.track_name
        #di["path"] = mpath+"/"+str(obj.track_path)
        di["path"] =str(obj.track_path.url)
        # print(di["path"])
        #di["image"] = mpath+"/"+str(obj.cover_image)
        di["image"] =str(obj.cover_image.url)
        return di

    clist = []

    for each in curplaylist:
        d = qtod(each)
        print(d)
        clist.append(d)

    print(clist)

    paginator= Paginator(musictrack.objects.all(),1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}

    jsonlist = json.dumps(clist)
    print("-------------------2")
    print(jsonlist)
    context = {'jsonlist':jsonlist}
   
    return render(request, 'musicplayer/music_player.html', context)



# #----------MUSIC player method--------------lists the music tracks
# def musicplayer2(request):
#     cat = request.user.guprofile.current_mood
#     tplaylist = playlist.objects.get(category_fk = cat)
#     print(tplaylist)

#     curplaylist = tplaylist.musictracks.all()
#     print("curr playlist")

#     print(settings.MEDIA_ROOT.replace('\\','/'))
#     tpath = settings.MEDIA_ROOT.replace('\\','/')
#     mpath = tpath.replace('MEDIA','media')

#     cplist = list(curplaylist.values())
#     #print(cplist)
#     jsonlist = serializers.serialize("json", tplaylist.musictracks.all(), fields=('track_name','track_path'))
#     #jsonlist = json.dumps(jsonlist)

#     def qtod(obj):
#         di = {}
#         di["name"] = obj.track_name
#         di["path"] = mpath+"/"+str(obj.track_path)
#         # print(di["path"])
#         di["image"] = mpath+"/"+str(obj.cover_image)
#         return di

#     clist = []

#     for each in curplaylist:
#         d = qtod(each)
#         print(d)
#         clist.append(d)

#     print(clist)

#     print(jsonlist)
#     context = {'jsonlist':clist}

#     paginator= Paginator(musictrack.objects.all(),1)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context={"page_obj":page_obj}

   
#     return render(request, 'musicplayer/music_player2.html', context)



# #------------One song player of the selected music track
# def onesongplayer(request,pk):
#     track = get_object_or_404(musictrack,id=pk)

#     context={'track':track}
#     return render(request, 'musicplayer/m_singleplayer.html',context)
#     editrev = music_reviews.objects.get(id=pk)
#     tid = editrev.track_fk.id
#     form = ReviewEditForm(instance = editrev)
#     if request.method =='POST':
#         form = ReviewEditForm(request.POST)
#         if form.is_valid():
#             editrev.review_text = form.cleaned_data['review_text']
#             editrev.save()
#             messages.success(request, "Successfully Edited your review!")
#             return redirect("reviews_list",tid)
#     context = {"form":form}
#     return render(request, 'musicplayer/m_singleplayer.html',context)




# #------------------------------------------------ajax search method not implemented but tried
# def music_search_list(request):
#     ctx = {}
#     url_parameter = request.GET.get("q")

#     if url_parameter:
#         tracks = musictrack.objects.filter(track_name__icontains=url_parameter)
#     else:
#         tracks = musictrack.objects.all()

#     print(tracks)
#     ctx["tracks"] = tracks
#     does_req_accept_json = request.accepts("application/json")
#     is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest" and does_req_accept_json

#     if is_ajax_request:

#         html = render_to_string(
#             template_name="musicplayer/tracks-results-partial.html", context={"tracks": tracks}
#         )
#         data_dict = {"html_from_view": html}
#         return JsonResponse(data=data_dict, safe=False)

#     return render(request, "musicplayer/search_results.html", context=ctx)