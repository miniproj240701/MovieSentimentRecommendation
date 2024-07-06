import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/movies')
      .then(response => response.json())
      .then(data => setMovies(data))
      .catch(error => console.error('Error fetching data:', error));
  }, []);

  return (
    <div className="App">
      <h1>Movies</h1>
      <ul>
        {movies.map(movie => (
          <li key={movie.id}>
            <h2>{movie.영화명}</h2>
            <img src={movie.포스터} alt={movie.영화명} />
            <p>Release Year: {movie.개봉년도}</p>
            <p>Rating: {movie.평점}</p>
            <p>Audience: {movie.관객수}</p>
            <p>Genre: {movie.장르}</p>
            <p>Running Time: {movie.상영시간}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
