from django.contrib import admin
from blog import views
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('page/<int:page>', views.index, name='index'),
    path('post/<slug:slug>', views.post_detail, name='post_detail'),
    path('tag/<slug:tag_title>', views.tag_filter, name='tag_filter'),
    path('contacts/', views.contacts, name='contacts'),
    path('', views.index, name='index'),
]  + debug_toolbar_urls()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
