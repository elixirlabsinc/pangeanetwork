import React, { Component } from 'react';
import styled from 'styled-components';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

const NavigationList = styled.ul`
  background-color: #262164;
  left: 0px;
  color: #ffffff;
  font-size: 13px;
  list-style-type: none;
  margin: 0px auto;
  padding: 0px;
  justify-content: center;
`;

const NavigationListItem = styled.li`
  display: inline;
  text-align: center;
  padding: 0px 60px
  justify-content: center;
  @media(min-width: 768px) and (max-width: 1080px) {
    padding: 0px 32px;
  }
  @media(max-width: 768px)  {
    display: block;
    padding: 12px 0px;
  }
`;

const NavigationLink = styled.a`
  color: #ffffff;
  font-size: 16px;
  text-decoration: none;
  padding: 0px 20px 4px 20px;
  &:active, &:hover {
    border-bottom: 4px solid #CEA02B;
  }
`;


class Navigation extends Component {
 
  render() {
    return (
      <Router>
      <NavigationList>
        <NavigationListItem>
            <NavigationLink href="/">
                <Link to="/">Dashboards</Link>
            </NavigationLink>
          </NavigationListItem>
        <NavigationListItem>
            <NavigationLink href="/coops">
                <Link to="/coops/">Co-Ops</Link>
            </NavigationLink>
          </NavigationListItem>
        <NavigationListItem>
            <NavigationLink href="/members">
                <Link to="/members/">Members</Link>
            </NavigationLink>
          </NavigationListItem>
        <NavigationListItem>
            <NavigationLink href="/transactions">
                <Link to="/transactions/">Transactions</Link>
            </NavigationLink>
          </NavigationListItem>
        <NavigationListItem>
            <NavigationLink href="/loans">
                <Link to="/loans/">Loans</Link>
            </NavigationLink>
          </NavigationListItem>
      </NavigationList>

      <Route path="/" exact component={this.Index} />
      <Route path="/coops/" component={this.Coops} />
      <Route path="/members/" component={this.Members} />
      <Route path="/transactions/" component={this.Transactions} />
      <Route path="/loans/" component={this.Loans} />

      
      </Router>
    );
  }


}

export default Navigation;
