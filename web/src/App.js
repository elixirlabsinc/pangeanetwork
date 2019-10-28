import React from 'react';
import Header from './components/header';
import Dashboard from './components/dashboard';
import Coops from './components/coops';
import Members from './components/members';
import Transactions from './components/transactions';
import RevolvingFund from './components/revolving_funds';
import ProtectedRoute from './components/protected_route';
import styled from 'styled-components';
import './styles/main.css';
import { BrowserRouter as Router, Route, Redirect, Switch } from "react-router-dom";


const PangeaNetworkDiv = styled.div`
`;

function App() {
  return (
    <PangeaNetworkDiv>
      <Header />
      <Router>
        <Switch>
          <Redirect exact from="/" to="/dashboard" />
          <ProtectedRoute path="/dashboard" component={Dashboard} />
          <ProtectedRoute path="/coops/" component={Coops} />
          <ProtectedRoute path="/members/" component={Members} />
          <ProtectedRoute path="/transactions/" component={Transactions} />
          <ProtectedRoute path="/revolving_funds/" component={RevolvingFund} />
          <Route render={() => <h1>404</h1>} />
        </Switch>
      </Router>
    </PangeaNetworkDiv> 
  );
}

export default App;
