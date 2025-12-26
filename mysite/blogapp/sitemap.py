from django.contrib.sitemaps import Sitemap

from .models import Article

class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Article.objects.filter(publishwd_at_isnull=False).order_by("-published_at")

    def lastmod(self, obj: Article):
        return obj.pk

