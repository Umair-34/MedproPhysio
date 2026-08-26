"""Wellness blog articles for Medpro Physiotherapy."""

BLOG_META_TITLE = 'Calgary Physiotherapy & Wellness Blog'
BLOG_META_DESCRIPTION = (
  'Guides on physiotherapy, massage, and wellness care at Medpro Physiotherapy '
  'in northwest Calgary.'
)

# Shared Savanna articles were removed. Add Medpro-only posts here.
BLOG_POSTS = []


def get_blog_posts():
  return BLOG_POSTS


def get_blog_post(slug):
  for post in BLOG_POSTS:
    if post['slug'] == slug:
      return post
  return None


def get_related_posts(slug, limit=2):
  return [post for post in BLOG_POSTS if post['slug'] != slug][:limit]
