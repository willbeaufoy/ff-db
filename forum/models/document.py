from base import *
from tag import Tag
from django.utils.translation import ugettext as _

class DocumentManager(NodeManager):
    def search(self, keywords, **kwargs):
        return False, self.filter(models.Q(title__icontains=keywords) | models.Q(body__icontains=keywords))

class Document(Node):
    class Meta(Node.Meta):
        proxy = True

    url = models.TextField(default='')
    organisation = models.TextField(default='')
    date_published = models.DateTimeField(null=True, blank=True)

    friendly_name = _("document")
    objects = DocumentManager()

    @property
    def closed(self):
        return self.nis.closed

    @property    
    def view_count(self):
        return self.extra_count

    @property
    def headline(self):
        return self._headline()

    def _headline(self):
        if self.nis.deleted:
            return _('[deleted] ') + self.title

        if self.nis.closed:
            return _('[closed] ') + self.title

        return self.title

    @property
    def accepted_answers(self):
        return self.answers.filter(~models.Q(state_string__contains="(deleted)"), marked=True)

    @models.permalink    
    def get_absolute_url(self):
        return ('question', (), {'id': self.id, 'slug': django_urlquote(slugify(self.title))})
        
    def meta_description(self):
        return self.summary

    def get_revision_url(self):
        return reverse('question_revisions', args=[self.id])

    def get_related_questions(self, count=10):
        cache_key = '%s.related_questions:%d:%d' % (settings.APP_URL, count, self.id)
        related_list = cache.get(cache_key)

        if related_list is None:
            related_list = Question.objects.filter_state(deleted=False).values('id').filter(tags__id__in=[t.id for t in self.tags.all()]
            ).exclude(id=self.id).annotate(frequency=models.Count('id')).order_by('-frequency')[:count]
            cache.set(cache_key, related_list, 60 * 60)

        return [Document.objects.get(id=r['id']) for r in related_list]
    



class DocumentSubscription(models.Model):
    user = models.ForeignKey(User)
    claim = models.ForeignKey(Node)
    auto_subscription = models.BooleanField(default=True)
    last_view = models.DateTimeField(default=datetime.datetime.now())

    class Meta:
        app_label = 'forum'


class DocumentRevision(NodeRevision):
    class Meta:
        proxy = True
        
