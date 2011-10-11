r"""

    occupywallst.urls
    ~~~~~~~~~~~~~~~~~

    HTTP request routing.

"""

from django.conf import settings
from django.conf.urls.defaults import patterns, url, include
from django.views.decorators.http import require_GET, require_POST

from occupywallst import admin, api, utils, feeds


adminsite = admin.AdminSite(name='occupyadmin')

urlpatterns = patterns('',
    url(r'^$', 'occupywallst.views.index', name='index'),
    url(r'^rss/news/$', feeds.RSSNewsFeed(), name='rss-news'),
    url(r'^rss/forum/$', feeds.RSSForumFeed(), name='rss-forum'),
    url(r'^rss/comments/$', feeds.RSSCommentFeed(), name='rss-comments'),
    url(r'^article/(?P<slug>[-_\d\w]+)/$', 'occupywallst.views.article', name='article'),
    url(r'^forum/$', 'occupywallst.views.forum', name='forum'),
    url(r'^forum/(?P<slug>[-_\d\w]+)/$', 'occupywallst.views.thread', name='forum-post'),
    url(r'^attendees/$', 'occupywallst.views.attendees', name='attendees'),
    url(r'^notification/(?P<id>\d+)/$', 'occupywallst.views.notification', name='notification'),
    url(r'^rides/$', 'occupywallst.views.rides', name='rides'),
    url(r'^rides/(?P<ride_id>\d+)/$', 'occupywallst.views.ride_info', name='ride_info'),
    url(r'^rides/create/$', 'occupywallst.views.ride_create', name='ride_create'),
    url(r'^rides/(?P<ride_id>\d+)/edit/$', 'occupywallst.views.ride_edit', name='ride_edit'),
    url(r'^rides/(?P<ride_id>\d+)/request/$', 'occupywallst.views.ride_request_add', name='ride_request'),
    url(r'^rides/(?P<ride_id>\d+)/request/delete/$', 'occupywallst.views.ride_request_delete', name='ride_request_delete'),
    url(r'^calendar/$', 'occupywallst.views.calendar', name='calendar'),
    url(r'^chat/$', 'occupywallst.views.chat', name='chat'),
    url(r'^chat/(?P<room>[a-zA-Z0-9]+)/$', 'occupywallst.views.chat', name='chat-private'),
    url(r'^housing/$', 'occupywallst.views.housing', name='housing'),
    url(r'^conference/$', 'occupywallst.views.conference', name='conference'),
    url(r'^about/$', 'occupywallst.views.about', name='about'),
    url(r'^login/$', 'occupywallst.views.login', name='login'),
    url(r'^logout/$', 'occupywallst.views.logout', name='logout'),
    url(r'^signup/$', 'occupywallst.views.signup', name='signup'),
    url(r'^error/$', 'occupywallst.views.error', name='error'),
    url(r'^users/(?P<username>[-_\d\w]+)/$', 'occupywallst.views.user_page', name='user'),
    url(r'^users/(?P<username>[-_\d\w]+)/edit/$', 'occupywallst.views.edit_profile', name='user-edit'),
    url(r'^api/safe/attendees/$', require_GET(utils.api_view(api.attendees))),
    url(r'^api/safe/attendee_info/$', require_GET(utils.api_view(api.attendee_info))),
    url(r'^api/safe/rides/$', require_GET(utils.api_view(api.rides))),
    url(r'^api/ride_request_update/$', require_POST(utils.api_view(api.ride_request_update)), name="ride_request_update"),
    url(r'^api/safe/article_get/$', require_GET(utils.api_view(api.article_get))),
    url(r'^api/safe/comment_get/$', utils.api_view(api.comment_get)),
    url(r'^api/safe/forumlinks/$', utils.api_view(api.forumlinks)),
    url(r'^api/safe/stock_data_get/$', utils.api_view(api.stock_data)),
    url(r'^api/article_new/$', require_POST(utils.api_view(api.article_new))),
    url(r'^api/article_edit/$', require_POST(utils.api_view(api.article_edit))),
    url(r'^api/article_delete/$', require_POST(utils.api_view(api.article_delete))),
    url(r'^api/comment_new/$', require_POST(utils.api_view(api.comment_new))),
    url(r'^api/comment_edit/$', require_POST(utils.api_view(api.comment_edit))),
    url(r'^api/comment_remove/$', require_POST(utils.api_view(api.comment_remove))),
    url(r'^api/comment_delete/$', require_POST(utils.api_view(api.comment_delete))),
    url(r'^api/comment_upvote/$', require_POST(utils.api_view(api.comment_upvote))),
    url(r'^api/comment_downvote/$', require_POST(utils.api_view(api.comment_downvote))),
    url(r'^api/message_send/$', require_POST(utils.api_view(api.message_send))),
    url(r'^api/message_delete/$', require_POST(utils.api_view(api.message_delete))),
    url(r'^api/check_username/$', require_POST(utils.api_view(api.check_username))),
    url(r'^api/signup/$', require_POST(utils.api_view(api.signup))),
    url(r'^api/login/$', require_POST(utils.api_view(api.login))),
    url(r'^api/logout/$', require_POST(utils.api_view(api.logout))),
    url(r'^admin/', include(adminsite.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
