from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Count, Q
from .models import Post
from .forms import CommentForm



# Create your views here.
class PostList(generic.ListView):
    """List of published posts.

    Uses `select_related` and `annotate` to reduce database queries and
    expose the approved comment count to the template as `approved_comments`.
    """
    model = Post
    template_name = "blog/index.html"
    paginate_by = 6

    def get_queryset(self):
        return (
            Post.objects.filter(status=1)
            .select_related('author')
            .annotate(approved_comments=Count('comments', filter=Q(comments__approved=True)))
            .order_by('-created_on')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.setdefault('subtitle', 'Latest posts from the Giddy Gardener')
        return ctx


def post_detail(request, slug):
    """
    Display an individual :model:`blog.Post`.

    **Context**

    ``post``
        An instance of :model:`blog.Post`.

    **Template:**

    :template:`blog/post_detail.html`
    """
    queryset = Post.objects.filter(status=1)
    post = get_object_or_404(queryset, slug=slug)
    
    comments = post.comments.all().order_by("-created_on")
    comment_count = post.comments.filter(approved=True).count()
    comment_form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {
            "post": post,
            "comments": comments,
            "comment_count": comment_count,
            "comment_form": comment_form,
         },
    )