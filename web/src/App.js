import React from 'react';
import Header from './components/header';
import Coops from './components/coops';
import Members from './components/members';
import Transactions from './components/transactions';
import Loans from './components/loans';
import styled from 'styled-components';
import './styles/main.css';
import { BrowserRouter as Router, Route } from "react-router-dom";
import RevolvingFund from './components/revolving_funds';


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
