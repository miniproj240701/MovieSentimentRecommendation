import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import styled from 'styled-components';
import { Container } from '@material-ui/core';
import ThumbUpAltIcon from '@material-ui/icons/ThumbUpAlt';
import ThumbDownAltIcon from '@material-ui/icons/ThumbDownAlt';
import GlobalStyle from '../globalStyles';
import { GradientLine } from '../gradientLine';
import ReactionBox from './ReactionBox';

interface Movie {
  id: number;
  영화명: string;
  개봉년도: string;
  장르: string;
  상영시간: string;
  줄거리: string;
  포스터: string;
  긍정비율: number;
  부정비율: number;
  등급: string;
  긍정워드클라우드: string[];
  부정워드클라우드: string[];
}

const MovieDetail = () => {
  const { id } = useParams<{ id?: string }>();
  const [movie, setMovie] = useState<Movie | null>(null);

  useEffect(() => {
    fetch('/긍부정영화정보리스트.json')
      .then(response => response.json())
      .then(data => {
        const foundMovie = data.find((movie: Movie) => movie.id === parseInt(id ?? '0'));
        setMovie(foundMovie);
      })
      .catch(error => console.error('Error loading movie data:', error));
  }, [id]);

  if (!movie) {
    return null; // 로딩 중일 때는 아무것도 렌더링하지 않음
  }

  return (
    <DetailContainer maxWidth={false}>
      <GlobalStyle />
      <Content>
        <PosterContainer>
          <Poster src={movie.포스터} alt={movie.영화명} />
        </PosterContainer>
        <Info>
          <MovieInfo>
            <MovieTitle>{movie.영화명}</MovieTitle>
            <InfoContainer>
              <TagContainer>
                <Tag className="highlight">{movie.등급.replace(/\D/g, '')}</Tag>
                <Tag>{movie.개봉년도}</Tag>
                <Tag>{movie.상영시간}</Tag>
                <Tag>{movie.장르}</Tag>
              </TagContainer>
              <Rating>
                {[1, 2, 3, 4, 5].map((star) => (
                  <Star key={star} $filled={star <= 5}>
                    <svg width="22" height="22" viewBox="0 0 22 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path
                        d="M8.14683 2.78116C9.04489 0.0172248 12.9551 0.0172229 13.8532 2.78115L14.3677 4.36474C14.7693 5.60081 15.9212 6.43769 17.2209 6.43769H18.886C21.7921 6.43769 23.0005 10.1565 20.6493 11.8647L19.3022 12.8435C18.2508 13.6074 17.8108 14.9615 18.2124 16.1976L18.727 17.7811C19.625 20.5451 16.4616 22.8435 14.1104 21.1353L12.7634 20.1565C11.7119 19.3926 10.2881 19.3926 9.23664 20.1565L7.88956 21.1353C5.53842 22.8435 2.37498 20.5451 3.27304 17.7812L3.78757 16.1976C4.1892 14.9615 3.74922 13.6074 2.69776 12.8435L1.35068 11.8647C-1.00046 10.1565 0.207867 6.43769 3.11404 6.43769H4.77912C6.0788 6.43769 7.23067 5.60081 7.63229 4.36475L8.14683 2.78116Z"
                        fill={star <= 5 ? '#D9D9D9' : 'none'}
                      />
                    </svg>
                  </Star>
                ))}
                <RatingText>평가하기</RatingText>
              </Rating>
            </InfoContainer>
            <GradientLine $thickness="5px" $marginTop="70px" $marginBottom="70px" />
            <Description>{movie.줄거리}</Description>
          </MovieInfo>
          <Statistics>
            <ReactionBox 
              isPositive={true}
              percentage={movie.긍정비율}
              wordCloud={movie.긍정워드클라우드}
            />
            <ReactionBox 
              isPositive={false}
              percentage={movie.부정비율}
              wordCloud={movie.부정워드클라우드}
            />
          </Statistics>
        </Info>
      </Content>
    </DetailContainer>
  );
};

const DetailContainer = styled(Container)`
  background-color: #000000;
  // min-height: 100vh;
  // padding: 40px 0;
`;

const Content = styled.div`
  display: flex;
  gap: 40px;
  color: #ffffff;
`;

const PosterContainer = styled.div`
  flex: 0 0 auto;
`;

const Poster = styled.img`
  width: 604px;
  height: 861px;
  object-fit: cover;
  border-radius: 5px;
`;

const Info = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
`;

const MovieInfo = styled.div`
  flex: 1;
`;


const MovieTitle = styled.h1`
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 700; /* S-Core Dream 6 Bold */
  font-size: 60px;
  margin-bottom: 10px;
  margin-top: 0; // 상단 마진 제거
`;

const Rating = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 20px;
`;

const Star = styled.div<{ $filled: boolean }>`
  width: 22px;
  height: 22px;
  margin-right: 5px;

  svg path {
    fill: ${props => (props.$filled ? '#D9D9D9' : 'none')};
  }
`;

const RatingText = styled.span`
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 500; // S-Core Dream 5 Medium
  font-size: 20px;
  color: #FFFFFF;
  margin-left: 10px;
`;

const InfoContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
`;

const TagContainer = styled.div`
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
`;

const Tag = styled.span`
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 500; // S-Core Dream 5 Medium
  font-size: 20px;
  color: #BABABA;
  padding: 5px 10px;
  border-radius: 5px;
  border: 1px solid #BABABA;
  background-color: transparent;

  &.highlight {
    // background-color: #ff6347;
    color: #ffffff;
    font-weight: bold;
    border-color: #ff6347;
  }
`;

const Description = styled.p`
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 400; // S-Core Dream 4 Regular
  font-size: 23px;
  line-height: 168%;
  color: #ffffff;
  margin-bottom: 30px;
`;

const Statistics = styled.div`
  display: flex;
  justify-content: space-between;
  gap: 20px;
  width: 100%;
`;

export default MovieDetail;
