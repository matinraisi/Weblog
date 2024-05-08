from django.shortcuts import render , get_object_or_404 ,redirect
from django.http import HttpResponse , Http404 
from .models import Post , Ticket , ImagePost
from .forms import *
from django.views.decorators.http import require_POST , require_GET
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView , DetailView
from django.db.models import Q
from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank ,TrigramSimilarity
from itertools import chain
# Create your views here.
def Home(request):
    return render(request , "blog/index.html" )

class PostListview(ListView):
    paginate_by = 3  
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "blog/list.html"

def Post_detail(request , id):
    post =  get_object_or_404(Post , id=id , status = Post.Status.PUBLISH)
    # try:
    #     post = Post.published.get(id=id)
    # except:
    #     raise Http404("not found post!...")
    form = CommentForm()
    comment = post.comments.filter(active =True)
    context = {
        "post" : post,
        "form" : form,
        "commetn":comment,
    }
    return render (request , "blog/detail.html" , context)
    
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(
                name = cd["name"],
                massege = cd["massege"],
                email = cd["email"],
                phone = cd["phone"],
                sunject = cd["sunject"],
                )
            return redirect("blog:index")
            
    else:
        form = TicketForm()
        # context = {
        #     "form" : form
        # }
    return render(request, "forms/ticket.html", {"form" : form})    

@require_POST
def post_comments(request , post_id):
    post = get_object_or_404(Post , id=post_id , status = Post.Status.PUBLISH) 
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        "post": post,
        "form" : form,
        "comment":comment
    }
    return render(request , "forms/comment.html" ,context) 

def crete_blog(request):
    if request.method == "POST":
        form = CratePost(request.POST , request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            img1 = ImagePost.objects.create(Image_file=form.cleaned_data['image1'] , post=post)
            post.images.add(img1)
            img2 = ImagePost.objects.create(Image_file=form.cleaned_data['image2'] , post=post)
            post.images.add(img2)
            post.save()
            return redirect("blog:index")
    else:
        form = CratePost()
    return render (request , "blog/createpost.html" , {"form" :form,})

@require_GET
def post_search(request):
    query=None
    result=[]
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # ============
            post_results = Post.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            image_post_results = ImagePost.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

            result = list(chain(post_results, image_post_results))
            # ==========
            # result = Post.objects.filter(description__search = query)
            # ===================
            # search_query = SearchQuery(query)
            # search_vector = SearchVector('title' , 'description')
            # result = Post.objects.annotate(search=search_vector , rank=SearchRank(search_vector,search_query)).filter(search  = search_query).order_by('-rank')
            #  SearchQuery(query) فارسی کامل پشتیبانی نمیشود
            # ====================
            # post_results = Post.objects.annotate(similarity=TrigramSimilarity('title', query) + TrigramSimilarity('description', query)).filter(similarity__gt=0.1).order_by('-similarity')
            # image_post_results = ImagePost.objects.annotate(similarity=TrigramSimilarity('title', query) + TrigramSimilarity('description', query)).filter(similarity__gt=0.1).order_by('-similarity')
            # result = list(chain(post_results, image_post_results))
    context = {
        'query':query,
        'result':result,
    }
    return render(request , 'blog/index.html' , context)

def profile(request):
    user = request.user
    post = Post.published.filter(author=user)
    # print(post)
    context = {
        'post':post,
    }
    return render(request , 'blog/profile.html' , context)


def delete_post(request, post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect("blog:profile")
    return render(request, 'forms/delete-post.html' , {post:'post'})

def delete_image(request, post_id):
    image = get_object_or_404(ImagePost,id=post_id)
    image.delete()
    return redirect("blog:profile")
    return render(request, 'forms/delete-image.html' , {image:'image'})
    
def edit_post(request, post_id):
    post = get_object_or_404(Post,id=post_id)
    if request.method == "POST":
            form = CratePost(request.POST , request.FILES , instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                img1 = ImagePost.objects.create(Image_file=form.cleaned_data['image1'] , post=post)
                post.images.add(img1)
                img2 = ImagePost.objects.create(Image_file=form.cleaned_data['image2'] , post=post)
                post.images.add(img2)
                post.save()
                return redirect("blog:index")
    else:
        form = CratePost( instance=post)
        return render (request , "blog/createpost.html" , {"form" :form, "post" :post})