from django.db.models import Count, Prefetch
from django.shortcuts import render, get_object_or_404
from blog.models import Comment, Post, Tag


def serialize_post(post):
    return {
        'title': post.title,
        'teaser_text': post.text[:200],
        'author': post.author.username,
        'comments_amount': post.num_comments,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in post.tags.all()],
        'first_tag_title': post.tags.first().title,
    }


def serialize_tag(tag):
    return {
        'title': tag.title,
        'posts_with_tag': tag.num_posts,
    }


def find_most_popular_posts():
    most_popular_posts = Post.objects.popular().author_and_tags_count()[:5]
    posts_with_comments = dict(Post.objects.fetch_with_comments_count().values_list('id', 'num_comments'))
    for post in most_popular_posts:
        post.num_comments = posts_with_comments[post.id]
    return most_popular_posts


def index(request):
    most_popular_posts = find_most_popular_posts()

    fresh_posts = (Post.objects.fetch_with_comments_count().
                   author_and_tags_count().order_by('published_at'))
    most_fresh_posts = list(fresh_posts)[-5:]

    most_popular_tags = Tag.objects.popular()[:5]

    context = {
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
        'page_posts': [serialize_post(post) for post in most_fresh_posts],
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
    }
    return render(request, 'index.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.annotate(num_likes=Count('likes')), slug=slug)
    comments = post.comments.prefetch_related('author',)
    serialized_comments = []
    for comment in comments:
        serialized_comments.append({
            'text': comment.text,
            'published_at': comment.published_at,
            'author': comment.author.username,
        })

    related_tags = post.tags.popular()

    serialized_post = {
        'title': post.title,
        'text': post.text,
        'author': post.author.username,
        'comments': serialized_comments,
        'likes_amount': post.num_likes,
        'image_url': post.image.url if post.image else None,
        'published_at': post.published_at,
        'slug': post.slug,
        'tags': [serialize_tag(tag) for tag in related_tags],
    }

    most_popular_tags = Tag.objects.popular()[:5]

    most_popular_posts = find_most_popular_posts()

    context = {
        'post': serialized_post,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'post-details.html', context)


def tag_filter(request, tag_title):
    all_tags = Tag.objects.all()
    tag = get_object_or_404(all_tags, title=tag_title)

    most_popular_tags = all_tags.popular()[:5]

    most_popular_posts = find_most_popular_posts()

    related_posts = Post.objects.filter(tags=tag).fetch_with_comments_count().author_and_tags_count()
    related_posts = related_posts[:20]

    context = {
        'tag': tag.title,
        'popular_tags': [serialize_tag(tag) for tag in most_popular_tags],
        'posts': [serialize_post(post) for post in related_posts],
        'most_popular_posts': [
            serialize_post(post) for post in most_popular_posts
        ],
    }
    return render(request, 'posts-list.html', context)


def contacts(request):
    # позже здесь будет код для статистики заходов на эту страницу
    # и для записи фидбека
    return render(request, 'contacts.html', {})



