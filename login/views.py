from django.shortcuts import render_to_response, render
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from login.models import User, Album, Photo
from login.forms import UploadForm, AlbumForm


@csrf_exempt
def signup(request):
    if request.POST:
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        u = User(username=username, email=email, password=password)
        u.save()
        return render_to_response('login/login.html')
    else:
        return render_to_response()

# import pdb; pdb.set_trace()

@csrf_exempt
def match(request):
    state = "Please log in below..."
    user_id = password = ''
    if request.method == 'POST':
        if request.POST.get('user_id'):
            user_id = int(request.POST.get('user_id'))
        if request.POST.get('password'):
            password = request.POST.get('password')
            # x=User.objects.filter(user_id=2)
            # Album.objects.get(album_id=16).delete()
            # Album.objects.get(album_id=18).delete()
            # import pdb;pdb.set_trace()

    # Retrieve records from table
        if user_id:
            u = User.objects.get(user_id=user_id)
            print u
            # Matching user_id and password
            if u.user_id == user_id and u.password == password:
                state = "Login successful"
                url = reverse('create_album', args=(user_id,))
                return HttpResponseRedirect(url)
            else:
                state = "Login failed"
        return render_to_response('login/login.html', {'state':state} )
    else:
        return render_to_response('login/login.html', {'state': state})


@csrf_exempt
def create_album(request, user_id):
    if request.method == 'POST':
        return create_album_post(request, user_id)
    else:
        form = AlbumForm()
        u = User.objects.filter(user_id=user_id)
        album_list = Album.objects.filter(user=u[0])
        # import pdb;pdb.set_trace()
        print (album_list)
        return render(request, 'login/album.html',{'album_list': album_list, 'form': form, 'user_id': user_id})


def create_album_post(request, user_id):
    form = AlbumForm()
    name = request.POST.get('name')
    u = User.objects.get(user_id=user_id)
    Album.objects.create(user=u, album_name=name)
    album_list = Album.objects.filter(user=u)
    print (album_list)
    return render(request, 'login/album.html', {'album_list': album_list, 'form': form, 'user_id': user_id})


@csrf_exempt
def upload_image(request, user_id, album_name):
    if request.method == 'POST':
        return upload_image_post(request, user_id, album_name)
    else:
        form = UploadForm() # An empty, unbound form
        a = Album.objects.filter(album_name=album_name)
        # Retrieving image list
        image_list = Photo.objects.filter(album=a[0])
        return render(request, 'login/list.html',{'image_list': image_list, 'form': form, 'album_name': album_name, 'user_id': user_id})


def upload_image_post(request, user_id, album_name):
    form = UploadForm(request.POST, request.FILES)
    if form.is_valid():
        a = Album.objects.filter(album_name=album_name, user=user_id)
        newdoc = Photo(album=a[0], image=request.FILES['docfile'])
        newdoc.save()
        image_list = Photo.objects.filter(album=a[0])
        return render(request, 'login/list.html', {'image_list': image_list, 'form': form, 'album_name': album_name, 'user_id': user_id})


@csrf_exempt
def delete_image(request):
    id=''
    if request.method == 'POST':
        form = UploadForm(request.POST)
        id = request.POST.get('id')
        album_name = request.POST.get('album_name')
        user_id = request.POST.get('user_id')
        # album_name = request.POST.get('album_name')
        Photo.objects.get(image_id=id).delete()
        a = Album.objects.filter(album_name=album_name, user_id=user_id)
        # Load documents for the list page
        image_list = Photo.objects.filter(album=a[0])
        return HttpResponseRedirect(reverse('upload', args=(user_id, album_name,)))


@csrf_exempt
def delete_album(request):
    id = ''
    if request.method == 'POST':
        form = AlbumForm(request.POST)
        id = request.POST.get('id')
        user_id = request.POST.get('user_id')
        Album.objects.get(album_id=id).delete()
    # import pdb;pdb.set_trace()
    u = User.objects.filter(user_id=user_id)
    album_list = Album.objects.filter(user=u[0])
    return HttpResponseRedirect(reverse('create_album', args=(user_id,)))

