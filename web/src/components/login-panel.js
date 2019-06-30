import React, { Component } from 'react';
import styled from 'styled-components';

const LoginPanelDiv = styled.div`
  background-color: #262164;
  position: absolute;
  right: 0px;
  padding: 0px 24px;
  color: #fff;
  font-size: 13px;
`;

const ProfileIcon = styled.img`
  width: 24px;
  height: 24px;
`;

class LoginPanel extends Component {
  render() {
    return (
      <LoginPanelDiv>
        <span>Jamie Liao</span>
        <span><ProfileIcon src="" /></span>
      </LoginPanelDiv>
    );
  }
}

export default LoginPanel;