import React, { Component } from 'react';
import styled from 'styled-components';

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
  @media(max-width: 600px) {
    display: block;
    padding: 12px 0px;
  }
`;

const NavigationLink = styled.a`
  color: #ffffff;
  font-size: 15px;
  text-decoration: none;
  padding-bottom: 4px;
  &:active, &:hover {
    border-bottom: 4px solid #CEA02B;
  }
`;


class Navigation extends Component {
  render() {
    return (
      <NavigationList>
        <NavigationListItem>
          <NavigationLink href="/">Dashboards</NavigationLink>
          </NavigationListItem>
        <NavigationListItem>
          <NavigationLink href="/coops">Co-Ops</NavigationLink>
          </NavigationListItem>
        <NavigationListItem>
          <NavigationLink href="/members">Members</NavigationLink>
          </NavigationListItem>
        <NavigationListItem>
          <NavigationLink href="/transactions">Transactions</NavigationLink>
          </NavigationListItem>
        <NavigationListItem>
          <NavigationLink href="/loans">Loans</NavigationLink>
          </NavigationListItem>
      </NavigationList>
    );
  }
}

export default Navigation;