import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import SearchIcon from '@material-ui/icons/Search';
import Search from './layouts/Search';
import { GradientLine } from '../gradientLine';
import { useNavigate } from 'react-router-dom';
import MovieItem from './MovieItem';

interface Movie {
  id: number;
  영화명: string;
  포스터: string;
  장르: string;
  추천영화?: {
    id: number;
    영화명: string;
    유사도: number;
    포스터: string;
  }[];
}

const MovieSelection: React.FC = () => {
  const [allMovies, setAllMovies] = useState<Movie[]>([]);
  const [displayedMovies, setDisplayedMovies] = useState<Movie[]>([]);
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const [movieIndex, setMovieIndex] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const moviesPerPage = 5;
  const [selectedMovieId, setSelectedMovieId] = useState<number | null>(null);
  const navigate = useNavigate();

  const comboBoxGenres = ['가족', '공포', '다큐멘터리', '드라마', '로맨스', '모험', '뮤지컬', '미스터리', '범죄', '서사', '서스펜스', '스릴러', '애니메이션', '액션', '전쟁', '코미디', '판타지'];
  const genreButtons = ['액션', 'SF', '로맨스', '코믹', '판타지', '공포', '스릴러'];

  useEffect(() => {
    fetch('/긍부정영화정보리스트.json')
      .then(response => response.json())
      .then((data: Movie[]) => {
        setAllMovies(data);
        setDisplayedMovies(data.slice(0, moviesPerPage)); // Initial display
      })
      .catch(error => console.error('Error loading movie data:', error));
  }, []);

  const handleMovieClick = (id: number) => {
    const movie = allMovies.find(m => m.id === id);
    if (movie) {
      setSelectedMovie(movie);
      setSelectedMovieId(id);
    }
  };

  const handleSearch = (term: string) => {
    setSearchTerm(term);
    filterMovies(term, selectedGenre);
  };

  const handleGenreClick = (genre: string) => {
    setSelectedGenre(genre);
    filterMovies(searchTerm, genre);
  };

  const filterMovies = (term: string, genre: string) => {
    let filtered = allMovies;
    if (genre) {
      filtered = filtered.filter(movie => movie.장르 === genre);
    }
    if (term) {
      filtered = filtered.filter(movie => 
        movie.영화명.toLowerCase().includes(term.toLowerCase())
      );
    }
    setDisplayedMovies(filtered);
    handlePageChange(1);
  };

  const handleSelectMovies = () => {
    if (selectedMovie && selectedMovie.추천영화) {
      const recommendedMovies = selectedMovie.추천영화.map(movie => ({
        id: movie.id,
        영화명: movie.영화명,
        포스터: movie.포스터,
      }));

      localStorage.setItem('recommendedMovies', JSON.stringify(recommendedMovies));
      
      navigate('/movie-list', {
        state: {
          selectedMovieId: selectedMovie.id,
          recommendedMovies: recommendedMovies,
        },
        replace: true
      });
    } else {
      console.log("No movie selected or no recommendations available");
    }
  };

  const handlePrev = () => {
    if (currentPage > 1) {
      handlePageChange(currentPage - 1);
    }
  };
  
  const handleNext = () => {
    const totalPages = Math.ceil(displayedMovies.length / moviesPerPage);
    if (currentPage < totalPages) {
      handlePageChange(currentPage + 1);
    }
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
    setMovieIndex((page - 1) * moviesPerPage);
  };

  const handleCancel = () => {
    navigate('/');
  };

  return (
    <Container>
      <Search 
        initialSearchText="최신 장르 검색" 
        searchType="combobox" 
        options={comboBoxGenres}
        onSearch={handleSearch}
      />
      <Title>추천 장르 선택</Title>
      <GenreContainer>
        {genreButtons.map(genre => (
          <GenreButton 
            key={genre} 
            onClick={() => handleGenreClick(genre)}
            selected={selectedGenre === genre}
          >
            {genre}
          </GenreButton>
        ))}
      </GenreContainer>
      <GradientLine $thickness="5px" $marginTop="70px" $marginBottom="70px" />
      
      <SubTitleContainer>
        <SubTitle></SubTitle>
        <SearchForm onSubmit={(e) => { e.preventDefault(); handleSearch(searchTerm); }}>
          <SearchInput 
            type="text" 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="최신 영화 검색"
          />
          <SearchButton type="submit">
            <SearchIcon />
          </SearchButton>
        </SearchForm>
      </SubTitleContainer>
      
      <MovieItem 
        title="추천 영화 선택"
        movies={displayedMovies}
        index={movieIndex}
        showLeftArrow={() => currentPage > 1}
        showRightArrow={() => currentPage < Math.ceil(displayedMovies.length / moviesPerPage)}
        handlePrev={handlePrev}
        handleNext={handleNext}
        onSelectMovie={handleMovieClick}
        selectedMovieId={selectedMovieId}
        showPagination={true}
        currentPage={currentPage}
        totalPages={Math.ceil(displayedMovies.length / moviesPerPage)}
        onPageChange={handlePageChange}
      />
      
      <ButtonContainer>
        <SelectButton onClick={handleSelectMovies}>영화 선택</SelectButton>
        <CancelButton onClick={handleCancel}>선택 안함</CancelButton>
      </ButtonContainer>
    </Container>
  );
};

const Container = styled.div`
  background-color: #000000;
  min-height: 100vh;
  padding: 20px;
  padding-bottom: 40px; // 하단에 약간의 여백 추가
`;

const Title = styled.h2`
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 700; // S-Core Dream 6 Bold
  font-size: 23px;
  color: #ffffff;
  margin-bottom: 20px;
`;

const SubTitleContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
`;

const SearchForm = styled.form`
  display: flex;
  margin-bottom: 30px; // 아래쪽 간격 추가
`;

const SearchInput = styled.input`
  width: 200px;
  height: 40px;
  padding: 10px;
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 500;
  font-size: 18px;
  border: none;
  border-radius: 5px 0 0 5px;
  background-color: #333333;
  color: #FFFFFF;

  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
  }

  &:focus {
    outline: none; // 포커스 시 나타나는 기본 외곽선 제거
  }
`;

const SearchButton = styled.button`
  background-color: #333333;
  color: #ffffff;
  border: none;
  padding: 10px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 0 5px 5px 0;
`;

const GenreContainer = styled.div`
  display: flex;
  justify-content: flex-start; // 왼쪽 정렬
  flex-wrap: wrap; // 여러 줄로 나뉘도록 설정
  gap: 10px; // 버튼 사이의 간격
  margin-bottom: 20px;
`;

const GenreButton = styled.button<{ selected: boolean }>`
  background-color: ${props => props.selected ? '#FF000' : '#B60000'};
  color: ${props => props.selected ? '#FF000' : '#ffffff'};
  border: none;
  padding: 10px 20px;
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 500; // S-Core Dream 5 Medium
  font-size: 18px;
  cursor: pointer;
  border-radius: 5px;
  margin-right: 10px;
  margin-bottom: 10px;
`;

const SubTitle = styled.h3`
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 700; // S-Core Dream 6 Bold
  font-size: 23px;
  color: #ffffff;
  margin-bottom: 20px;
`;

const ButtonContainer = styled.div`
  display: flex;
  justify-content: center;
  gap: 41px; // 버튼 사이 간격
  margin-top: 115px; // 상단 마진 추가
`;

const SelectButton = styled.button`
  width: 136px; // 버튼 너비
  height: 39px; // 버튼 높이
  background-color: #B60000;
  color: #ffffff;
  border: none;
  font-size: 16px; // 폰트 크기 16px
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 700; // S-Core Dream 6 Bold
  cursor: pointer;
  border-radius: 5px;
`;

const CancelButton = styled(SelectButton)`
  background-color: #333333;
`;

export default MovieSelection;
