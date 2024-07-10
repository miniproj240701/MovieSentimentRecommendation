import React from 'react'
import styled from 'styled-components'
import { AppBar, Toolbar } from '@material-ui/core'
import Title from './Title'
import Search from './Search'

const Header = () => {
  return (
    <StyledAppBar position="static">
      <StyledToolbar>
        <Title />
      </StyledToolbar>
    </StyledAppBar>
  )
}

const StyledAppBar = styled(AppBar)`
  && {
    background-color: #1c1c1c;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
  }
`

const StyledToolbar = styled(Toolbar)`
  // display: flex;
  // justify-content: space-between;
  // align-items: center;
  // margin-left: 78px;
`

export default Header