import styled from 'styled-components';

interface GradientLineProps {
  $thickness?: string;
  $marginTop?: string;
  $marginBottom?: string;
}

export const GradientLine = styled.div<GradientLineProps>`
  width: 100%;
  max-width: 100vw;
  height: ${props => props.$thickness || '1px'};
  background: linear-gradient(to right, #870000 0%, #210000 100%);
  margin: 0 auto;
  margin-top: ${props => props.$marginTop || '0'};
  margin-bottom: ${props => props.$marginBottom || '0'};
`;
