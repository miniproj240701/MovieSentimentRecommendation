import { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  :root {
    --primary-color: #6200ea;
    --secondary-color: #03dac6;
    --background-color: #1e1e1e;
    --font-color: #fff;
    --font-size: 16px;
    --font-family: 'Roboto', sans-serif;
  }

  body {
    margin: 0;
    padding: 0;
    background-color: var(--background-color);
    color: var(--font-color);
    font-size: var(--font-size);
    font-family: var(--font-family);
  }

  h1, h2, h3, h4, h5, h6 {
    color: var(--font-color);
  }

  a {
    color: var(--primary-color);
  }

  a:hover {
    color: var(--secondary-color);
  }

  .gradient-line {
    width: 100%;
    max-width: 1920px;
    height: 1px;
    background: linear-gradient(to right, #870000 0%, #210000 100%);
    margin: 0 auto;
  }
`;

export default GlobalStyle;
