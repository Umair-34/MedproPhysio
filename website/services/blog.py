from datetime import date
from html import escape

from website import blog_content
from website.models import BlogPost


def sections_to_html(sections):
    """Convert legacy section JSON into HTML for the Summernote editor."""
    chunks = []
    for section in sections or []:
        heading = section.get('heading')
        if heading:
            chunks.append(f'<h2>{escape(heading)}</h2>')
        for paragraph in section.get('paragraphs', []):
            chunks.append(f'<p>{escape(paragraph)}</p>')
        items = section.get('list') or []
        if items:
            list_items = ''.join(f'<li>{escape(item)}</li>' for item in items)
            chunks.append(f'<ul>{list_items}</ul>')
        blockquote = section.get('blockquote')
        if blockquote:
            chunks.append(f'<blockquote><p>{escape(blockquote)}</p></blockquote>')
    return '\n'.join(chunks)


def backfill_blog_content_from_sections():
    """Populate empty content fields from legacy section data."""
    updated = 0
    for post in BlogPost.objects.filter(content=''):
        if post.sections:
            post.content = sections_to_html(post.sections)
            post.save(update_fields=['content', 'updated_at'])
            updated += 1
    return updated


def sync_legacy_blog_posts():
    """Import coded blog articles into the database (idempotent)."""
    for post in blog_content.BLOG_POSTS:
        faqs = [list(item) for item in post.get('faqs', [])]
        sections = post.get('sections', [])
        BlogPost.objects.update_or_create(
            slug=post['slug'],
            defaults={
                'title': post['title'],
                'meta_title': post.get('meta_title', post['title']),
                'meta_description': post.get('meta_description', ''),
                'summary': post.get('summary', ''),
                'tag': post.get('tag', ''),
                'image': post.get('image', ''),
                'image_alt': post.get('image_alt', ''),
                'published_date': date.fromisoformat(post['published_date']),
                'author': post.get('author', 'Medpro Physiotherapy Team'),
                'reading_time': post.get('reading_time', '5 min read'),
                'content': sections_to_html(sections),
                'key_takeaways': post.get('key_takeaways', []),
                'sections': sections,
                'faqs': faqs,
                'related_services': post.get('related_services', []),
                'is_published': True,
            },
        )
    backfill_blog_content_from_sections()


def get_blog_posts():
    posts = BlogPost.objects.filter(is_published=True).order_by('-published_date', '-created_at')
    if posts.exists():
        return [post.to_public_dict() for post in posts]
    return blog_content.get_blog_posts()


def get_blog_post(slug):
    try:
        post = BlogPost.objects.get(slug=slug, is_published=True)
        return post.to_public_dict()
    except BlogPost.DoesNotExist:
        return blog_content.get_blog_post(slug)


def get_related_posts(slug, limit=2):
    posts = BlogPost.objects.filter(is_published=True).exclude(slug=slug).order_by(
        '-published_date',
    )[:limit]
    if posts.exists():
        return [post.to_public_dict() for post in posts]
    return blog_content.get_related_posts(slug, limit=limit)
