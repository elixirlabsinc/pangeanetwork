import React from 'react';
import logo from './logo.svg';
import Header from './components/header';
import Content from './components/content';
import styled from 'styled-components';
import './styles/main.css';

const PangeaNetworkDiv = styled.div`
`;

function App() {
  return (
    <PangeaNetworkDiv>
      <Header />
      <Content />
    </PangeaNetworkDiv>
  );
}

export default App;
