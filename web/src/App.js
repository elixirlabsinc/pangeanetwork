import React from 'react';
import logo from './logo.svg';
import Header from './components/header';
import Content from './components/content';
import Transactions from './components/transactions';
import styled from 'styled-components';
import './styles/main.css';
import RevolvingFund from './components/revolving_funds';

const PangeaNetworkDiv = styled.div`
`;

function App() {
  const action = window.location.pathname;
  const content = action === '/members' ? <Content /> : <Transactions />
  return (
    <PangeaNetworkDiv>
      <Header />
      {content}
    </PangeaNetworkDiv>
  );
}

export default App;
