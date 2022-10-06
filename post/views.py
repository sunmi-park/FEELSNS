from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import Postedit, CommentForm
from django.views.generic import ListView, TemplateView


def main_page(request):
    posts = Post.objects.order_by('-id')
    return render(request, 'main_page.html', {'posts':posts})


@login_required
def make_post(request):
    return render(request, 'make_post.html')

@login_required
def create_post(request):
    user = request.user
    post = Post()
    post.title = request.POST.get('title')
    post.body = request.POST.get('body')
    post.pub_date = timezone.datetime.now()
    post.nickname = user
    post.save()
    return redirect('/detailed_post/' + str(post.id))


@login_required
def detailed_post(request, post_id):
    post_detail = get_object_or_404(Post, pk=post_id)
    write_comment = Comment.objects.filter(post_id=post_id).order_by('-created_at')
    return render(request, 'detailed_post.html', {'post': post_detail, 'comment': write_comment})

@login_required
def new_post(request):
    full_text = request.GET['fulltext']

    word_list = full_text.split()

    word_dictionary = {}

    for word in word_list:
        if word in word_dictionary:
            # Increase
            word_dictionary[word] += 1
        else:
            # add to the dictionary
            word_dictionary[word] = 1

    return render(request, 'make_post.html', {'fulltext': full_text, 'total': len(word_list), 'dictionary': word_dictionary.items()} )

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.method =='POST':
        form = Postedit(request.POST)
        if form.is_valid():
            user = request.user
            post.title = form.cleaned_data['title']
            post.body = form.cleaned_data['body']
            post.pub_date=timezone.now()
            post.nickname = user
            post.save()
            return redirect('/detailed_post/' + str(post.id))
    else:
        form = Postedit(instance = post)
 
        return render(request,'edit_post.html', {'form':form})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('/')

def write_comment(request, post_id):
    if request.method == 'POST':
        comment = request.POST.get('comment','')
        current_post = Post.objects.get(id=post_id)

        C = Comment()
        C.comment = comment
        C.nickname = request.user
        C.post = current_post
        C.save()

        return redirect('/detailed_post/'+str(post_id))

@login_required
def delete_comment(request, post_id):
    comment = Comment.objects.get(id=post_id)
    comment.delete()
    return redirect('/detailed_post/'+str(post_id))