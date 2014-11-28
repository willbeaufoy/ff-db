from django.conf.urls import patterns, url, include
from django.utils.translation import ugettext as _
from django.conf import settings

urlpatterns = patterns('',
    (r'', include('forum.urls')),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns = patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    ) + urlpatterns

# urlpatterns = urlpatterns + url(r'^send-selection$', app.writers.send_selection, name='send_selection'),


handler404 = 'forum.views.meta.page'
handler500 = 'forum.views.meta.error_handler'
