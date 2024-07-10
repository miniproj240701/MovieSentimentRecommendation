import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { useLocation, useNavigate } from 'react-router-dom';
import { GradientLine } from '../gradientLine';
import Search from './layouts/Search';
import MovieItem from './MovieItem';

interface Movie {
  id: number;
  영화명: string;
  포스터: string;
  관객수: number;
  개봉년도: string;
  평점: string;
  장르: string;
  리뷰: { 작성자: string; 작성일: string; 별점: string; 리뷰내용: string; }[];
}

const MovieList = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [recommendedMovies, setRecommendedMovies] = useState<Movie[]>([]);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [filteredMovies, setFilteredMovies] = useState<Movie[]>([]);
  const [topIndex, setTopIndex] = useState(0);
  const [newIndex, setNewIndex] = useState(0);
  const [recommendedIndex, setRecommendedIndex] = useState(0);
  const [selectedRecommendedMovieId, setSelectedRecommendedMovieId] = useState<number | null>(null);
  const [selectedTopMovieId, setSelectedTopMovieId] = useState<number | null>(null);
  const [selectedNewMovieId, setSelectedNewMovieId] = useState<number | null>(null);

  // 모든 영화 데이터 로드
  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await fetch('/긍부정영화정보리스트.json');
        const data = await response.json();
        console.log("Movies loaded:", data.length);
        setMovies(data);
      } catch (error) {
        console.error('Error loading movie data:', error);
      }
    };

    fetchMovies();
  }, []);

  // 추천 영화 관리
  useEffect(() => {
    const updateRecommendedMovies = () => {
      let newRecommendedMovies: Movie[] = [];

      // localStorage에서 추천 영화 확인
      const storedRecommendedMovies = localStorage.getItem('recommendedMovies');
      if (storedRecommendedMovies) {
        newRecommendedMovies = JSON.parse(storedRecommendedMovies);
        console.log("Recommended movies from localStorage:", newRecommendedMovies.length);
      }

      // location.state에서 추천 영화 확인 (새로운 추천이 있는 경우)
      if (location.state && location.state.recommendedMovies) {
        newRecommendedMovies = location.state.recommendedMovies;
        console.log("New recommended movies from location state:", newRecommendedMovies.length);
        
        // 새로운 추천 영화를 localStorage에 저장
        localStorage.setItem('recommendedMovies', JSON.stringify(newRecommendedMovies));
      }

      // 추천 영화 업데이트
      if (newRecommendedMovies.length > 0) {
        setRecommendedMovies(newRecommendedMovies);
        console.log("Updated recommended movies:", newRecommendedMovies.length);
      }
    };

    updateRecommendedMovies();
  }, [location.state]);
  
  const handlePrev = (section: 'top' | 'new' | 'recommended') => {
    if (section === 'top') {
      setTopIndex(prev => Math.max(prev - 5, 0));
    } else if (section === 'new') {
      setNewIndex(prev => Math.max(prev - 5, 0));
    } else if (section === 'recommended') {
      setRecommendedIndex(prev => Math.max(prev - 5, 0));
    }
  };

  const handleNext = (section: 'top' | 'new' | 'recommended') => {
    const maxIndex = section === 'top' ? Math.max(topMovies.length - 5, 0) 
                  : section === 'new' ? Math.max(newMovies.length - 5, 0)
                  : Math.max(recommendedMovies.length - 5, 0);
    if (section === 'recommended') {
      setRecommendedIndex(prev => Math.min(prev + 5, maxIndex));
    } else if (section === 'top') {
      setTopIndex(prev => Math.min(prev + 5, maxIndex));
    } else if (section === 'new') {
      setNewIndex(prev => Math.min(prev + 5, maxIndex));
    }
  };

  const calculatePopularity = (movie: Movie) => {
    const currentYear = 2023;
    const releaseYear = parseInt(movie.개봉년도);

    const audienceScore = Math.min(movie.관객수 / 10000000, 1) * 40;
    const ratingScore = parseFloat(movie.평점) * 3;
    const reviewScore = Math.min(Math.log(movie.리뷰.length) * 5, 20);
    const yearWeight = currentYear - releaseYear <= 3 ? 10 - ((currentYear - releaseYear) * 2) : 0;

    return audienceScore + ratingScore + reviewScore + yearWeight;
  };

  /** 인기도 점수 기준 정렬 */
  const sortedMovies = [...movies].sort((a, b) => calculatePopularity(b) - calculatePopularity(a));
  const topMovies = sortedMovies.slice(0, 10);

  /** 개봉년도 기준 정렬 */
  const newMovies = [...movies].sort((a, b) => parseInt(b.개봉년도) - parseInt(a.개봉년도)).slice(0, 10);

  const [recommendedCurrentPage, setRecommendedCurrentPage] = useState(1);
  const [topCurrentPage, setTopCurrentPage] = useState(1);
  const [newCurrentPage, setNewCurrentPage] = useState(1);

  const moviesPerPage = 5;
  const recommendedTotalPages = Math.ceil(recommendedMovies.length / moviesPerPage);
  const topTotalPages = Math.ceil(topMovies.length / moviesPerPage);
  const newTotalPages = Math.ceil(newMovies.length / moviesPerPage);

  const handlePageChange = (page: number, section: 'recommended' | 'top' | 'new') => {
    switch(section) {
      case 'recommended':
        setRecommendedCurrentPage(page);
        setRecommendedIndex((page - 1) * moviesPerPage);
        break;
      case 'top':
        setTopCurrentPage(page);
        setTopIndex((page - 1) * moviesPerPage);
        break;
      case 'new':
        setNewCurrentPage(page);
        setNewIndex((page - 1) * moviesPerPage);
        break;
    }
  };

  const handleSelectMovie = (id: number, section: 'recommended' | 'top' | 'new') => {
    console.log("Selected movie ID:", id);
    // setSelectedMovieId(id);
    
    switch(section) {
      case 'recommended':
        setSelectedRecommendedMovieId(id);
        break;
      case 'top':
        setSelectedTopMovieId(id);
        break;
      case 'new':
        setSelectedNewMovieId(id);
        break;
    }
    
    const selectedMovie = movies.find(movie => movie.id === id);
    if (selectedMovie) {
      setFilteredMovies(movies.filter(movie => movie.장르 === selectedMovie.장르));
      
      navigate(`/movie/${id}`, { 
        state: { 
          selectedMovie,
          recommendedMovies: recommendedMovies
        } 
      });
    } else {
      console.error(`Movie with id ${id} not found`);
    }
  };

  const handleSearch = (term: string) => {
    console.log("Search term:", term);
    navigate('/movie-selection', { state: { searchTerm: term } });
  };

  console.log("Rendering MovieList. Recommended movies count:", recommendedMovies.length);

  return (
    <Container>
      <Search 
        initialSearchText="영화 선호도 검색" 
        searchType="button" 
        options={[]} 
        onSearch={handleSearch} 
      />
      {recommendedMovies.length > 0 && (
        <>
          <MovieItem 
            title="추천 Top 10"
            movies={recommendedMovies}
            index={recommendedIndex}
            showLeftArrow={index => index > 0}
            showRightArrow={(index, totalLength) => index < Math.max(totalLength - 5, 0)}
            handlePrev={() => handlePrev('recommended')}
            handleNext={() => handleNext('recommended')}
            onSelectMovie={(id) => handleSelectMovie(id, 'recommended')}
            selectedMovieId={selectedRecommendedMovieId}
            currentPage={recommendedCurrentPage}
            totalPages={recommendedTotalPages}
            onPageChange={(page) => handlePageChange(page, 'recommended')}
          />
          <GradientLine $thickness="2px" $marginTop="20px" $marginBottom="20px" />
        </>
      )}

      <MovieItem 
        title="인기 Top 10"
        movies={topMovies}
        index={topIndex}
        showLeftArrow={index => index > 0}
        showRightArrow={(index, totalLength) => index < Math.max(totalLength - 5, 0)}
        handlePrev={() => handlePrev('top')}
        handleNext={() =>  handleNext('top')}
        onSelectMovie={(id) => handleSelectMovie(id, 'top')}
        selectedMovieId={selectedTopMovieId}
        currentPage={topCurrentPage}
        totalPages={topTotalPages}
        onPageChange={(page) => handlePageChange(page, 'top')}
      />

      <GradientLine $thickness="5px" $marginTop="20px" $marginBottom="20px" />
      
      <MovieItem 
        title="최신영화"
        movies={newMovies}
        index={newIndex}
        showLeftArrow={index => index > 0}
        showRightArrow={(index, totalLength) => index < Math.max(totalLength - 5, 0)}
        handlePrev={() => handlePrev('new')}
        handleNext={() => handleNext('new')}
        onSelectMovie={(id) => handleSelectMovie(id, 'new')}
        selectedMovieId={selectedNewMovieId}
        currentPage={newCurrentPage}
        totalPages={newTotalPages}
        onPageChange={(page) => handlePageChange(page, 'new')}
      />
    </Container>
  );
};

const Container = styled.div`
  background-color: #000;
  padding: 11px;
`;

export default MovieList;
