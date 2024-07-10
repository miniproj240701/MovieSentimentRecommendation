import React from 'react';
import styled from 'styled-components';
import ThumbUpAltIcon from '@material-ui/icons/ThumbUpAlt';
import ThumbDownAltIcon from '@material-ui/icons/ThumbDownAlt';

interface ReactionBoxProps {
  isPositive: boolean;
  percentage: number;
  wordCloud: string[];
}

const ReactionBox: React.FC<ReactionBoxProps> = ({ isPositive, percentage, wordCloud }) => {
  return (
    <StatBox $positive={isPositive}>
      <LeftContent>
        <ReactionText>{isPositive ? '긍정적 반응' : '부정적 반응'}</ReactionText>
        <Percentage>{percentage}%</Percentage>
        <WordCloud>
          {wordCloud.slice(0, 4).map((word, index) => (
            <Word key={index} $positive={isPositive}>{word}</Word>
          ))}
        </WordCloud>
      </LeftContent>
      <RightContent>
        <ThumbIcon $positive={isPositive}>
          {isPositive ? <ThumbUpAltIcon /> : <ThumbDownAltIcon />}
        </ThumbIcon>
      </RightContent>
    </StatBox>
  );
};

const StatBox = styled.div<{ $positive?: boolean }>`
  display: flex;
  justify-content: space-between;
  padding: 20px;
  border-radius: 15px;
  background-color: ${props => props.$positive ? '#004016' : '#390000'};
  width: 489px;
  height: 255px;
  box-sizing: border-box;
`;

const LeftContent = styled.div`
  flex: 1;
`;

const RightContent = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-left: 20px;
`;

const ReactionText = styled.div`
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 500;
  font-size: 30px;
  color: #ffffff;
  margin-bottom: 15px;
`;

const ThumbIcon = styled.div<{ $positive?: boolean }>`
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10px;

  svg {
    font-size: 111px;
  }
`;

const Percentage = styled.span`
  font-family: 'Roboto', sans-serif;
  font-weight: 700;
  font-size: 64px;
  color: #ffffff;
  margin-bottom: 39px;
`;

const WordCloud = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
`;

const Word = styled.span<{ $positive?: boolean }>`
  font-family: 'S-Core Dream', sans-serif;
  font-weight: 500;
  font-size: 14px;
  padding: 5px 10px;
  background-color: ${props => props.$positive ? '#4caf50' : '#f44336'};
  color: #ffffff;
  border-radius: 20px;
`;

export default ReactionBox;