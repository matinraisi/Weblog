from django.shortcuts import render , get_object_or_404 ,redirect
from django.http import HttpResponse , Http404
from .models import Post , Ticket
from .forms import *

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView , DetailView
# Create your views here.
def Home(request):
    return HttpResponse("home page ")

""" """
# def Post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, 2)
#     page_number = request.GET.get('page',1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     context = {
#         "posts" : posts,
#     }
#     return render(request , "blog/list.html" , context )

class PostListview(ListView):
    paginate_by = 3  
    queryset = Post.published.all()
    context_object_name = "posts"
    template_name = "blog/list.html"

""""""
# ----------------------------------------
# class PostDitailview(DetailView):
#     model = Post
#     template_name = "blog/detail.html"   
def Post_detail(request , id):
    post =  get_object_or_404(Post , id=id , status = Post.Status.PUBLISH)
    # try:
    #     post = Post.published.get(id=id)
    # except:
    #     raise Http404("not found post!...")
    context = {
        "post" : post,
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
