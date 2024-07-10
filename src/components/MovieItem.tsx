import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';
import KeyboardArrowLeftIcon from '@material-ui/icons/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@material-ui/icons/KeyboardArrowRight';

interface Movie {
  id: number;
  포스터: string;
  영화명: string;
}

interface MovieItemProps {
  title: string;
  movies: Movie[];
  index: number;
  showLeftArrow: (index: number) => boolean;
  showRightArrow: (index: number, totalLength: number) => boolean;
  handlePrev: () => void;
  handleNext: () => void;
  onSelectMovie: (id: number) => void;
  onPageChange: (page: number) => void;
  currentPage: number;
  totalPages: number;
  selectedMovieId: number | null;
  showPagination?: boolean;
}

const MovieItem = ({
  title,
  movies,
  index,
  showLeftArrow,
  showRightArrow,
  handlePrev,
  handleNext,
  onSelectMovie,
  onPageChange,
  currentPage,
  totalPages,
  selectedMovieId,
  showPagination = false
}: MovieItemProps) => {
  const [isAtEnd, setIsAtEnd] = useState(false);
  const observerRef = useRef<IntersectionObserver | null>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsAtEnd(entry.isIntersecting);
      },
      {
        root: null,
        threshold: 0.1,
        rootMargin: '0px 0px 0px 0px', // Adjust rootMargin to detect when the element is at the bottom of the screen
      }
    );

    const lastMovieCard = document.querySelector('.movie-card:last-child');
    if (lastMovieCard) {
      observer.observe(lastMovieCard);
    }

    observerRef.current = observer;

    return () => {
      if (observerRef.current && lastMovieCard) {
        observerRef.current.unobserve(lastMovieCard);
      }
    };
  }, [movies, index]);

  const renderPageNumbers = () => {
    const pageNumbers = [];
    const maxVisiblePages = 5; // 한 번에 표시할 최대 페이지 수

    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

    if (endPage - startPage + 1 < maxVisiblePages) {
      startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }

    if (startPage > 1) {
      pageNumbers.push(
        <PageNumber key="first" onClick={() => handlePageClick(1)} $active={currentPage === 1}>
          1
        </PageNumber>
      );
      if (startPage > 2) {
        pageNumbers.push(<Ellipsis key="ellipsis1">...</Ellipsis>);
      }
    }

    for (let i = startPage; i <= endPage; i++) {
      pageNumbers.push(
        <PageNumber key={i} onClick={() => handlePageClick(i)} $active={i === currentPage}>
          {i}
        </PageNumber>
      );
    }

    if (endPage < totalPages) {
      if (endPage < totalPages - 1) {
        pageNumbers.push(<Ellipsis key="ellipsis2">...</Ellipsis>);
      }
      pageNumbers.push(
        <PageNumber key="last" onClick={() => handlePageClick(totalPages)} $active={currentPage === totalPages}>
          {totalPages}
        </PageNumber>
      );
    }

    return pageNumbers;
  };

  const handlePageClick = (page: number) => {
    onPageChange(page);
  };

  return (
    <Section>
      <Title>{title}</Title>
      <MovieCarouselWrapper>
        {showLeftArrow(index) && (
          <ArrowWrapper $left>
            <Arrow onClick={handlePrev}>
              <KeyboardArrowLeftIcon />
            </Arrow>
          </ArrowWrapper>
        )}
        <MovieCarousel>
          <MovieGrid>
            {movies.slice(index, index + 5).map((movie, movieIndex) => (
              <MovieCard
                key={movie.id}
                onClick={() => onSelectMovie(movie.id)}
                $selected={movie.id === selectedMovieId}
                className={movieIndex === movies.slice(index, index + 5).length - 1 ? 'movie-card' : ''}
              >
                <PosterWrapper $selected={movie.id === selectedMovieId}>
                  <Poster src={movie.포스터} alt={movie.영화명} $selected={movie.id === selectedMovieId} />
                  {movieIndex === movies.slice(index, index + 5).length - 1 && (
                    <FadeOverlay $isAtEnd={isAtEnd} />
                  )}
                </PosterWrapper>
              </MovieCard>
            ))}
          </MovieGrid>
        </MovieCarousel>
        {showRightArrow(index, movies.length) && (
          <ArrowWrapper $right>
            <Arrow onClick={handleNext}>
              <KeyboardArrowRightIcon />
            </Arrow>
          </ArrowWrapper>
        )}
      </MovieCarouselWrapper>
      {showPagination && totalPages > 1 && (
        <Pagination>{renderPageNumbers()}</Pagination>
      )}
    </Section>
  );
};

const Section = styled.section`
  margin-bottom: 20px;
`;

const Title = styled.h2`
  font-size: 24px;
  margin-bottom: 16px;
  margin-left: 10px;
`;

const MovieCarouselWrapper = styled.div`
  position: relative;
  margin-left: -20px;
  overflow: visible;
`;

const MovieCard = styled.div<{ $selected: boolean }>`
  flex: 0 0 auto;
  width: ${props => (props.$selected ? '357px' : '258px')};
  height: ${props => (props.$selected ? '508px' : '370px')};
  margin-top: ${props => (props.$selected ? '2px' : '47px')};
  cursor: pointer;
  transition: transform 0.3s ease, width 0.3s ease, height 0.3s ease, margin-top 0.3s ease;
  position: relative;
  transform: ${props => (props.$selected ? 'scale(1.0)' : 'scale(1)')};
  z-index: ${props => (props.$selected ? 10 : 0)};

  &:hover {
    transform: ${props => (props.$selected ? 'scale(1.0)' : 'scale(1.05)')};
  }
`;

const PosterWrapper = styled.div<{ $selected: boolean }>`
  position: relative;
  width: 100%;
  height: 100%;
`;

const Poster = styled.img<{ $selected: boolean }>`
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 5px;
`;

const FadeOverlay = styled.div<{ $isAtEnd: boolean }>`
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 30%;
  background: ${props =>
    props.$isAtEnd
      ? 'linear-gradient(to top, rgba(0, 0, 0, 0.8) 0%, rgba(0, 0, 0, 0) 100%)'
      : 'none'};
  pointer-events: none;
  transition: background 0.3s ease;
`;

const ArrowWrapper = styled.div<{ $left?: boolean; $right?: boolean }>`
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  ${props => props.$left && 'left: 0;'}
  ${props => props.$right && 'right: 0;'}
  z-index: 1;
`;

const MovieCarousel = styled.div`
  overflow: visible;
`;

const MovieGrid = styled.div`
  display: flex;
  justify-content: center;
  gap: 95px; /* 좌우 간격 설정 */
`;

const Arrow = styled.button`
  background: none;
  border: none;
  color: #fff;
  cursor: pointer;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Pagination = styled.div`
  display: flex;
  justify-content: center;
  margin-top: 20px;
`;

const PageNumber = styled.span<{ $active: boolean }>`
  color: ${props => (props.$active ? '#ff0000' : '#fff')};
  font-size: 14px;
  margin: 0 5px;
  cursor: pointer;
  font-weight: ${props => (props.$active ? 'bold' : 'normal')};

  &:hover {
    text-decoration: underline;
  }
`;

const Ellipsis = styled.span`
  color: #fff;
  margin: 0 5px;
`;

export default MovieItem;
