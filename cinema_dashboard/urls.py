from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('add_rooms/', views.add_room, name='add_room'),
    path('movies/<int:room_id>/', views.movie, name='movie'),
    path('add_movie/<int:room_id>/', views.add_movie, name='add_movie'),
    path('remove_movie/<int:movie_id>/<int:room_id>/', views.remove_movie, name='remove_movie'),
    path('remove_room/<int:room_id>/', views.remove_room, name='remove_room'),
    path('admin_dashboard/', views.admin_dashboard, name='admin'),
    path('rooms/', views.RoomListView.as_view(), name='room-list'),
    path('movies_list/', views.movies_list, name='movie-list'),
    path('book_seat/<int:movie_id>/', views.book_seat, name='book_seat'),
    path('select_seat/<int:movie_id>/<int:seat_id>/', views.select_seat, name='select_seat'),  # Book a specific seat
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
