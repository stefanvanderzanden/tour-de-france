from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

import game.views as game_views
from game.views import RennerView, RennerFormView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'TourDeFrance.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/', RennerView.as_view()),
    url(r'^home_alternative/', game_views.home, {}, 'home'),
    url(r'^add_renner/', RennerFormView.as_view()),

)
