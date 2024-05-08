panle 
user = blog
pass =  blog1234

matin==pass==>Hani1234
<!-- ===================== -->
<!-- parcice -->
tmrin --> 
1--> برای ایجاد پست فرم بنویس 
2-->اعتبار سنجی هم انجام بشه 
3-->نشون دادن خطاها در تمپلیت

4-->تمپلیت تگ پستی ک بیشترین زمان مطالعه رو نیاز داره همراه با کمترین زمان 
5--> فیلتر مینویسیم که کلمات رو سانسور کنه مثلا ستاره بزاره بجاش 
6--> تمپلیت تگ که فعال ترین کاربر رو داره به اصطلاح بیشترین پست رو گذاشته در ایندکس
7-->

<!-- ================================ -->
functions for views tets
1-
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

2- 
# def crete_post(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             Post.objects.create(
#                 title = cd['title'],
#                 author = cd['author'],
#                 slug = cd['slug'],
#                 status = cd['status'],
#                 reading_time = cd['reading_time'],
#                 description = cd['description'],
#             )
#             return redirect("blog:index")
#         # else:
#         #      print(form.errors)
#     else:
#         form = PostForm()
#     return render (request , "blog/createpost.html" , {"form" :form,})

3 - class base views
# ----------------------------------------
# class PostDitailview(DetailView):
#     model = Post
#     template_name = "blog/detail.html"   