from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# ---------------- IN-MEMORY DATA ----------------
users = []
movies = []
shows = []
bookings = []

# ---------------- Pydantic Models ----------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class MovieCreate(BaseModel):
    name: str
    genre: str
    duration: str

class ShowCreate(BaseModel):
    movie_id: int
    time: str
    date: str

class BookingCreate(BaseModel):
    user_id: int
    show_id: int
    seats: str
    price: int

class MovieUpdate(BaseModel):
    name: str | None = None
    genre: str | None = None
    duration: str | None = None

# ---------------- Helper Functions ----------------
def find_user(user_id):
    for u in users:
        if u["id"] == user_id:
            return u
    return None

def find_movie(movie_id):
    for m in movies:
        if m["id"] == movie_id:
            return m
    return None

def find_show(show_id):
    for s in shows:
        if s["id"] == show_id:
            return s
    return None

def filter_logic(name=None, genre=None):
    result = movies

    if name is not None:
        result = [m for m in result if name.lower() in m["name"].lower()]

    if genre is not None:
        result = [m for m in result if genre.lower() in m["genre"].lower()]

    return result

# ---------------- GET ROUTES ----------------
@app.get("/")
def home():
    return {"message": "Movie Booking API Running"}

@app.get("/movies")
def get_movies(search: str = "", page: int = 1, limit: int = 2):

    # FILTER (same as before)
    result = [
        m for m in movies
        if search.lower() in m["name"].lower()
        or search.lower() in m["genre"].lower()
    ]

    total_items = len(result)

    # CALCULATE TOTAL PAGES
    total_pages = (total_items + limit - 1) // limit

    if total_items == 0:
        return {"message": "No movies found"}

    # PAGINATION LOGIC
    start = (page - 1) * limit
    end = start + limit

    paginated_data = result[start:end]

    return {
        "page": page,
        "limit": limit,
        "total_items": total_items,
        "total_pages": total_pages,
        "data": paginated_data
    }

@app.get("/bookings")
def get_bookings():
    return bookings

@app.get("/summary")
def summary():
    return {
        "total_users": len(users),
        "total_movies": len(movies),
        "total_shows": len(shows),
        "total_bookings": len(bookings)
    }

@app.get("/filter-movies")
def filter_movies(name: str = None, genre: str = None):
    return filter_logic(name, genre)

# ---------------- POST ROUTES ----------------
@app.post("/create-user")
def create_user(user: UserCreate):
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email,
        "password": user.password
    }
    users.append(new_user)
    return new_user

@app.post("/add-movie", status_code=201)
def add_movie(movie: MovieCreate):
    for m in movies:
        if m["name"].lower() == movie.name.lower():
            raise HTTPException(status_code=400, detail="Movie already exists")

    new_movie = {
        "id": len(movies) + 1,
        "name": movie.name,
        "genre": movie.genre,
        "duration": movie.duration
    }
    
    movies.append(new_movie)
    return new_movie

@app.post("/add-show")
def add_show(show: ShowCreate):
    if not find_movie(show.movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")

    new_show = {
        "id": len(shows) + 1,
        "movie_id": show.movie_id,
        "time": show.time,
        "date": show.date
    }
    shows.append(new_show)
    return new_show

@app.post("/book-ticket")
def book_ticket(booking: BookingCreate):
    if not find_user(booking.user_id):
        raise HTTPException(status_code=404, detail="User not found")

    if not find_show(booking.show_id):
        raise HTTPException(status_code=404, detail="Show not found")

    if booking.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than 0")

    new_booking = {
        "id": len(bookings) + 1,
        "user_id": booking.user_id,
        "show_id": booking.show_id,
        "seats": booking.seats,
        "price": booking.price
    }

    bookings.append(new_booking)
    return new_booking

# ---------------- WORKFLOW ENDPOINT (Q14) ----------------
@app.post("/full-booking")
def full_booking(user_id: int, movie_id: int, seats: str, price: int):

    user = find_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    selected_show = None
    for s in shows:
        if s["movie_id"] == movie_id:
            selected_show = s
            break

    if not selected_show:
        raise HTTPException(status_code=404, detail="No show available for this movie")

    if price <= 0:
        raise HTTPException(status_code=400, detail="Invalid price")

    new_booking = {
        "id": len(bookings) + 1,
        "user_id": user_id,
        "show_id": selected_show["id"],
        "seats": seats,
        "price": price
    }

    bookings.append(new_booking)

    return {
        "message": "Full booking successful",
        "booking": new_booking
    }

# ---------------- CRUD (Movie) ----------------
@app.put("/update-movie/{movie_id}")
def update_movie(movie_id: int, movie: MovieUpdate):
    existing = find_movie(movie_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Movie not found")

    if movie.name is not None:
        existing["name"] = movie.name

    if movie.genre is not None:
        existing["genre"] = movie.genre

    if movie.duration is not None:
        existing["duration"] = movie.duration

    return existing

@app.delete("/delete-movie/{movie_id}")
def delete_movie(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    for s in shows:
        if s["movie_id"] == movie_id:
            raise HTTPException(
                status_code=400,
                detail="Cannot delete movie with active shows"
            )

    movies.remove(movie)
    return {"message": "Movie deleted successfully"}

@app.get("/sort-movies")
def sort_movies(sort_by: str = "name", order: str = "asc"):

    # VALIDATE sort_by
    valid_fields = ["name", "genre", "duration"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    # VALIDATE order
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    reverse = True if order == "desc" else False

    sorted_movies = sorted(movies, key=lambda x: x[sort_by], reverse=reverse)

    if not sorted_movies:
        return {"message": "No movies available to sort"}

    return sorted_movies

@app.get("/bookings-advanced")
def bookings_advanced(
    user_id: int = None,
    show_id: int = None,
    sort_by: str = "id",
    order: str = "asc",
    page: int = 1,
    limit: int = 2
):

    result = bookings

    # 🔍 SEARCH (FILTER)
    if user_id is not None:
        result = [b for b in result if b["user_id"] == user_id]

    if show_id is not None:
        result = [b for b in result if b["show_id"] == show_id]

    # 🔽 SORT
    if sort_by not in ["id", "user_id", "show_id", "price"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # 📄 PAGINATION
    total_items = len(result)
    total_pages = (total_items + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_data = result[start:end]

    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "data": paginated_data
    }

@app.get("/browse")
def browse(
    search: str = None,
    genre: str = None,
    sort_by: str = "name",
    order: str = "asc",
    page: int = 1,
    limit: int = 2
):

    result = movies

    # 🔍 SEARCH + FILTER
    if search is not None:
        result = [
            m for m in result
            if search.lower() in m["name"].lower()
            or search.lower() in m["genre"].lower()
        ]

    if genre is not None:
        result = [m for m in result if genre.lower() in m["genre"].lower()]

    # 🔽 SORT
    if sort_by not in ["name", "genre", "duration"]:
        raise HTTPException(status_code=400, detail="Invalid sort field")

    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order")

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # 📄 PAGINATION
    total_items = len(result)
    total_pages = (total_items + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    paginated_data = result[start:end]

    if not result:
        return {"message": "No movies found"}

    return {
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items,
        "data": paginated_data
    }
# ---------------- VARIABLE ROUTE (LAST) ----------------
@app.get("/movies/{movie_id}")
def get_movie_by_id(movie_id: int):
    movie = find_movie(movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie