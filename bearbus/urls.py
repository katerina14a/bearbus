from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'bus.views.home', name='home'),
    url(r'^stops/$', 'bus.views.stops'),
    url(r'^logout/$', 'bus.views.logout'),
    url(r'^register/$', 'bus.views.register'),
    url(r'^saved_stops/$', 'bus.views.saved_stops'),
    url(r'^login/$', 'bus.views.login_user'),
    url(r'^routes/$', 'bus.views.routes'),
    #    (r'^polls/(?P<poll_id>\d+)/results/$', 'mysite.views.results'),
    url(r'^routes/(?P<route_id>\w+)/$', 'bus.views.route_stops'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
