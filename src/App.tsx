import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import MovieList from './components/MovieList';
import MovieDetail from './components/MovieDetail';
import MovieSelection from './components/MovieSelection';
import GlobalStyle from './globalStyles';
import Header from './components/layouts/Header';
import styled from 'styled-components';

const App = () => {
  return (
    <>
      <GlobalStyle />
      <Header />
      <MainContent>
        <Routes>
          <Route path="/" element={<MovieList />} />
          <Route path="/movie/:id" element={<MovieDetail />} />
          <Route path="/movie-selection" element={<MovieSelection />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </MainContent>
    </>
  );
};

export default App;

const MainContent = styled.div`
  padding-top: 78px; // AppBar의 기본 높이
`