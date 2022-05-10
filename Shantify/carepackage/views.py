from django.shortcuts import render, redirect,get_object_or_404
from django.db.models import Q
from django.contrib.auth.models import User

from .models import carepack, therapist, packsubscribe
from accounts.models import GUprofile

# packlist method to diaplay the pack object list 
def packlist(request):
    packs = carepack.objects.all()
    context = {"packs":packs,"nbar":'carepacks'}
    return render(request, 'carepackages/package_pack_list.html',context)

# packinfo method to diaplay the pack object info
def packinfo(request,pk):
    try:
        packone = get_object_or_404(carepack, id=pk)
    except:
        packone=None
    subscribed = packsubscribe.objects.filter(suser = request.user, pack_subscribed = packone);

    if request.method =='POST':
        if packone:
            tempsub = packsubscribe.objects.filter(suser = request.user, pack_subscribed = packone);
            if tempsub:
                print("already subcribed")
                print( packone.subscribed_count)
                tempsub.delete()
                packone.subscribed_count -=1
                packone.save()
            else:
                newsubs = packsubscribe.objects.create(suser = request.user, pack_subscribed = packone, completed=False)
                newsubs.save()
                packone.subscribed_count +=1
                packone.save()

            return redirect('packinfo', pk)


    context = {"pack":packone,"subscribed":subscribed,"nbar":"carepacks"}
    return render(request, 'carepackages/package_pack_info.html',context)

# therapistlist method to diaplay the therapist object list 
def therapistlist(request):
    tpists = therapist.objects.all()
    context = {"tpists":tpists,"nbar":"therapistlist"}
    return render(request, 'carepackages/package_therapist_list.html',context)

# therapistinfo method to diaplay the therapist object info
def therapistinfo(request,pk):
    tpist = get_object_or_404(therapist, id=pk)
    context = {"tpist":tpist,"nbar":"therapistlist"}
    return render(request, 'carepackages/package_therapist_info.html',context)

# display my subscried packs
def mysubs(request):
    packs = packsubscribe.objects.filter(suser = request.user)
    print(packs)
    
    #packs = packs.objects.filter()
    context = {"packs":packs,"nbar":"mysubs"}
    return render(request, 'carepackages/package_mysubs.html',context)

# display list of songs of the subscribed playlist
def packageplaylist(request,pk):
    packs = carepack.objects.get(id = pk)

    context = {"packs":packs,"nbar":"packageplaylist"}
    return render(request, 'carepackages/package_playlist.html',context)

# display the pdf of a particular care package
def packagepdf(request,pk):
    try:
        pack = carepack.objects.get(id = pk)
    except:
        pack = None

    context = {"pack":pack,"nbar":"packageplaylist"}
    return render(request, 'carepackages/package_playlist.html',context)

