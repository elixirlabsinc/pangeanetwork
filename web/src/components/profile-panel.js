import React, { Component } from 'react';
import styled from 'styled-components';
import profileIcon from '../img/profileIcon.png'

const ProfilePanelDiv = styled.div`
  background-color: #262164;
  float: right;
  padding: 0px 24px;
  color: #fff;
  font-size: 14px;
`;

const ProfileLink = styled.a`
  padding: 0px 12px;
  color: #ffffff;
  text-decoration: none;
`;

const ProfileIcon = styled.img`
  width: 24px;
  height: 24px;
  vertical-align: middle;
`;

class ProfilePanel extends Component {
  render() {
    return (
      <ProfilePanelDiv>
        <ProfileLink href="/">Jamie Liao</ProfileLink>
        <ProfileIcon src={profileIcon} />
      </ProfilePanelDiv>
    );
  }
}

export default ProfilePanel;