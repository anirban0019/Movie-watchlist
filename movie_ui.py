import tkinter as tk
from tkinter import messagebox
import requests

TMDB_API_KEY = "03c66155bff05c0c3c2eea47dddaedd3"
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

API_BASE_URL = "http://127.0.0.1:8000/api/movies/"

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Watchlist")
        self.root.geometry("500x500")

        # Title Label
        tk.Label(root, text="Movie Watchlist", font=("Arial", 16, "bold")).pack(pady=10)

        # Movie Details Input
        tk.Label(root, text="Title:").pack()
        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        tk.Label(root, text="Genre:").pack()
        self.genre_entry = tk.Entry(root)
        self.genre_entry.pack()

        tk.Label(root, text="Release Year:").pack()
        self.year_entry = tk.Entry(root)
        self.year_entry.pack()

        tk.Button(root, text="Fetch Details", command=self.fetch_movie_details).pack(pady=5)
        # Buttons
        tk.Button(root, text="Add Movie", command=self.add_movie).pack(pady=5)
        tk.Button(root, text="Show Movies", command=self.show_movies).pack(pady=5)

        # Movie List
        self.movie_listbox = tk.Listbox(root, width=50, height=10)
        self.movie_listbox.pack(pady=10)
        self.movie_listbox.bind("<Double-Button-1>", self.change_status)

        # Delete Button
        tk.Button(root, text="Delete Selected", command=self.delete_movie).pack(pady=5)

        self.show_movies()

    def add_movie(self):
        """Add a new movie via API."""
        title = self.title_entry.get()
        genre = self.genre_entry.get()
        year = self.year_entry.get()

        if not (title and genre and year.isdigit()):
            messagebox.showerror("Error", "Please provide valid movie details.")
            return

        response = requests.post(API_BASE_URL + "add/", json={
            "title": title, "genre": genre, "release_year": int(year)
        })

        if response.status_code == 201:
            messagebox.showinfo("Success", "Movie added successfully!")
            self.show_movies()
        else:
            messagebox.showerror("Error", "Failed to add movie.")

    def show_movies(self):
        """Retrieve and display movies."""
        self.movie_listbox.delete(0, tk.END)
        response = requests.get(API_BASE_URL + "list/")

        if response.status_code == 200:
            movies = response.json()
            for movie in movies:
                display_text = f"{movie['id']} - {movie['title']} ({movie['release_year']}) - {movie['status']}"
                self.movie_listbox.insert(tk.END, display_text)

    def change_status(self, event):
        """Mark movie as watched or to watch."""
        selected = self.movie_listbox.curselection()
        if not selected:
            return

        movie_text = self.movie_listbox.get(selected[0])
        movie_id = movie_text.split(" - ")[0]
        new_status = "Watched" if "To Watch" in movie_text else "To Watch"

        response = requests.post(API_BASE_URL + f"update/{movie_id}/", json={"status": new_status})

        if response.status_code == 200:
            messagebox.showinfo("Success", "Movie status updated!")
            self.show_movies()
        else:
            messagebox.showerror("Error", "Failed to update status.")

    def delete_movie(self):
        """Delete selected movie."""
        selected = self.movie_listbox.curselection()
        if not selected:
            return

        movie_text = self.movie_listbox.get(selected[0])
        movie_id = movie_text.split(" - ")[0]

        response = requests.post(API_BASE_URL + f"delete/{movie_id}/")

        if response.status_code == 200:
            messagebox.showinfo("Success", "Movie deleted!")
            self.show_movies()
        else:
            messagebox.showerror("Error", "Failed to delete movie.")
    def fetch_movie_details(self):
        """Fetch movie details from TMDb API."""
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Enter a movie title.")
            return

        params = {
            "api_key": TMDB_API_KEY,
            "query": title
        }
        response = requests.get(TMDB_SEARCH_URL, params=params)
        
        if response.status_code == 200:
            results = response.json().get("results", [])
            if results:
                movie = results[0]  # Get the first search result
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, movie["title"])

                self.genre_entry.delete(0, tk.END)
                self.genre_entry.insert(0, "N/A")  # TMDb doesn't provide genre in search

                self.year_entry.delete(0, tk.END)
                self.year_entry.insert(0, movie["release_date"].split("-")[0])

                messagebox.showinfo("Success", "Movie details fetched!")
            else:
                messagebox.showerror("Error", "No movie found.")
        else:
            messagebox.showerror("Error", "Failed to fetch movie details.")


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()
