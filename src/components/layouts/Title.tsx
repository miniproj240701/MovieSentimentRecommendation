import React from 'react'
import styled from 'styled-components'
import { Link } from 'react-router-dom'

const Title = () => {
  return (
    <TitleWrapper>
        <StyledLink to="/">
            <svg viewBox="0 0 200 100" width="200" height="100">
                <defs>
                <filter id="shadow">
                    <feMorphology in="SourceAlpha" result="DILATED" operator="dilate" radius="10"/>
                    <feFlood floodColor="#990000" floodOpacity="1" result="SHADOW"/>
                    <feComposite in="SHADOW" in2="DILATED" operator="in" result="SHADOW_FILTER"/>
                    <feMerge>
                    <feMergeNode in="SHADOW_FILTER"/>
                    <feMergeNode in="SourceGraphic"/>
                    </feMerge>
                </filter>
                </defs>
                <text
                x="10"
                y="75"
                fontFamily="'Rammetto One', sans-serif"
                fontSize="80"
                fill="#FF0000"
                filter="url(#shadow)"
                letterSpacing="1"
                >
                IT's
                </text>
            </svg>
        </StyledLink>
    </TitleWrapper>
  )
}

const TitleWrapper = styled.div`
  svg {
    width: 114px;
    height: 72px;

    // @media (max-width: 1920px) {
    //   height: calc(100vh * 0.0926);
    // }

    // @media (max-width: 1280px) {
    //   height: calc(100vh * 0.0741);
    // }

    // @media (max-width: 768px) {
    //   height: calc(100vh * 0.0556);
    // }

    // @media (max-width: 480px) {
    //   height: calc(100vh * 0.0463);
    // }
  }
`

const StyledLink = styled(Link)`
  text-decoration: none;
  color: inherit;
  cursor: pointer;
`

export default Title