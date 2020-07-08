from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import CommentForm
from . models import Video
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# def index(request):
#     videos = Video.objects.all()
#     context = {"videos":videos}
#     return render(request, 'index.html', context)

def index(request):
    videos = Video.objects.all().order_by('-created')[:10]
    paginator = Paginator(videos, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)
    context = {
        'videos': videos,
        'queryset': paginated_queryset,
        'page_request_var': page_request_var,
    }
    return render(request, 'index.html', context)

def detail(request,title):
    post_list = Video.objects.filter(title=title)
    video_data = Video.objects.all()

    #CommentForm
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.post = post_list
            obj.save()
            return redirect('detail',title=post_list.title)
    else:
        form = CommentForm()

    context = {'post_list': post_list, 'allvideos':video_data, 'form':form}
    return render(request, 'details.html', context,)


def search(request):
    query = request.GET.get('q')
    if query:
        queryset = Video.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(author__icontains=query)
        ).distinct()
    context = {
        'queryset':queryset
    }
    return render(request, 'search_results.html', context)

# def like(request,id):
#     u_name = register.objects.get(username=request.session['username'])
#     video = myVideos.objects.get(id=id)
#     if video.likes.filter(id=u_name.id).exists():
#         return redirect('show', video.title)
#     else:
#         if video.dislikes.filter(id=u_name.id).exists():
#             video.dislikes.remove(u_name)
#             video.likes.add(u_name)
#             return redirect('show', video.title)
#         else:
#             video.likes.add(u_name)
#             return redirect('show', video.title)
#
#
# def dislike(request,id):
#     u_name = register.objects.get(username=request.session['username'])
#     video = myVideos.objects.get(id=id)
#     if video.dislikes.filter(id=u_name.id).exists():
#         return redirect('show', video.title)
#
#
#     else:
#         if video.likes.filter(id=u_name.id).exists():
#             video.likes.remove(u_name)
#             video.dislikes.add(u_name)
#             return redirect('show', video.title)
#         else:
#             video.dislikes.add(u_name)
#             return redirect('show', video.title)
#
# def comment(request):
#     text = request.POST['comment']
#     id=request.POST['v_id']
#     if text and id:
#         u_name = register.objects.get(username=request.session['username'])
#         video = myVideos.objects.get(id=id)
#         obj=comments(user_name=u_name,videoid=video,comment=text)
#         obj.save()
#         return redirect('show', video.title)