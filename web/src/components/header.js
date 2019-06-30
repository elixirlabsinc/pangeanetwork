import React, { Component } from 'react';
import styled from 'styled-components';
import LoginPanel from './profile-panel'
import Titles from './titles'
import Navigation from './navigation'

const HeaderDiv = styled.div`
  background-color: #262164;
  padding: 20px 10px;
  width: 100%;
`;

const HeaderContent = styled.div`
  margin: auto;
  width: 80%;
  text-align: center;
`;

class Header extends Component {
  render() {
    return (
      <HeaderDiv>
        <HeaderContent>
          <LoginPanel />
          <Titles />
          <Navigation />
        </HeaderContent>
      </HeaderDiv>
    );
  }
}

export default Header;