import React from 'react';
import logo from './logo.svg';
import Header from './components/header';
import Content from './components/content';
import Transactions from './components/transactions';
import styled from 'styled-components';
import './styles/main.css';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

const PangeaNetworkDiv = styled.div`
`;

function App() {
  return (
    <PangeaNetworkDiv>
      <Header />
      <Router>
        <Route path="/coops/" component={Coops} />
        <Route path="/members/" component={Members} />
        <Route path="/transactions/" component={Transactions} />
        <Route path="/loans/" component={Loans} />
      </Router>
    </PangeaNetworkDiv> 
  );
}

export default App;
