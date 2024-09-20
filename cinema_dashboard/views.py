from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Room, Movie, Seat
from .forms import SignUpForm, RoomForm, MovieForm
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    return render(request, 'admin_auth/login.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.is_superuser = True
            user.save()
            return redirect('admin')
    else:
        form = SignUpForm()
    return render(request, 'admin_auth/signup.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


def admin_dashboard(request):
    all_rooms = Room.objects.all()
    print(all_rooms)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(all_rooms)  # This will print all rooms to your console
            return render(request, 'admin_auth/admin_dashboard.html',
                          {'rooms': all_rooms})  # Use render to pass context
        else:
            return render(request, 'admin_auth/login.html', {'error': 'Invalid credentials'})

    return render(request, 'admin_auth/admin_dashboard.html', {'rooms': all_rooms})


def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            new_device = form.save()
            new_device_id = new_device.id

            return redirect('/admin_dashboard/')
    else:
        form = RoomForm()
    return render(request, 'admin_auth/add_room.html', {'form': form})


def add_movie(request, room_id):
    room = Room.objects.get(id=room_id)  # Fetch the specific room

    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        print(form.errors)

        if form.is_valid():
            new_movie = form.save(commit=False)
            new_movie.room = room
            new_movie.save()
            create_seats_for_movie(new_movie, room.rows, room.columns)

            return redirect(f'/movies/{room_id}')
    else:
        form = RoomForm()
    return render(request, 'admin_auth/add_movies.html', {'form': form, 'room_id': room_id})


def create_seats_for_movie(movie, rows, columns):
    for row in range(1, rows+1):
        for number in range(1, columns+1):
            Seat.objects.create(movie=movie, row=row, number=number)


def movie(request, room_id):
    device = get_object_or_404(Room, pk=room_id)
    try:
        cells_for_device = Movie.objects.filter(room=device).order_by("id")
        print(cells_for_device)
    except Exception as e:
        print(e)
        print(f'No movies in Room: {room_id}')
        cells_for_device = []
    return render(request, 'admin_auth/movies.html', {'room': device, 'movies': cells_for_device})


def remove_movie(request, movie_id, room_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect(f'/movies/{room_id}')


def remove_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    room.delete()
    return redirect(f'/admin_dashboard/')


# List rooms
class RoomListView(ListView):
    model = Room
    template_name = 'cinema/room_list.html'


def movies_list(request):
    all_movies = Movie.objects.all()
    return render(request, 'cinema/movie_list.html', {'all_movies': all_movies})


def book_seat(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    # Get all seats associated with this movie
    seats = Seat.objects.filter(movie=movie)

    # Optionally, group seats by row (if you want to organize them by row)
    grouped_seats = {}
    for seat in seats:
        if seat.row not in grouped_seats:
            grouped_seats[seat.row] = []
        grouped_seats[seat.row].append(seat)

    return render(request, 'cinema/book_seat.html', {
        'movie': movie,
        'grouped_seats': grouped_seats,  # Pass the grouped seats to the template
    })


# List seats for a specific movie
def SeatListView(request, pk):
    print(f'Movie ID: {pk}')
    movie = get_object_or_404(Movie, pk=pk)
    seats = Seat.objects.filter(movie=movie)
    context = {
        'seats': seats,
        'movie': movie,
    }
    return render(request, 'cinema/seat_list.html', context)


# Book a seat
def select_seat(request, movie_id, seat_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seat = get_object_or_404(Seat, id=seat_id, movie=movie)

    # Mark the seat as unavailable once booked
    if seat.status == 'available':
        seat.status = 'unavailable'
        seat.save()

    return redirect('book_seat', movie_id=movie.id)