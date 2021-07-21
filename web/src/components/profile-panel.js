import React, { Component } from 'react';
import styled from 'styled-components';
import profileIcon from '../img/profileIcon.png'

const ProfilePanelDiv = styled.a`
  background-color: #262164;
  float: right;
  color: #fff;
  font-size: 14px;
  padding: 8px 12px;
  color: #ffffff;
  text-decoration: none;
  &:active, &:hover {
    border-bottom: 4px solid #CEA02B;
  }
`;

const ProfileLink = styled.span`
  padding: 0px 12px;
`;

const ProfileIcon = styled.img`
  width: 24px;
  height: 24px;
  vertical-align: middle;
`;

class ProfilePanel extends Component {
  render() {
    return (
      <ProfilePanelDiv href="/">
        <ProfileLink>Admin User</ProfileLink>
        <ProfileIcon src={profileIcon} />
      </ProfilePanelDiv>
    );
  }
}

export default ProfilePanel;