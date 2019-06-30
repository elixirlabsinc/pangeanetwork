import React, { Component } from 'react';
import styled from 'styled-components';

const TitlesDiv = styled.div`
  padding: 24px;
`;

const SiteTitle = styled.div`
  font-size: 1.8em;
  letter-spacing: 14%;
  color: #ffffff;
  line-height: 28px;
  padding: 48px 0px 12px 0px;
`;

const SubTitle = styled.div`
  text-transform: uppercase;
  letter-spacing: 14%;
  font-size: 1.2em;
  color: #CEA02B;
`;

class Titles extends Component {
  render() {
    return (
      <TitlesDiv>
          <SiteTitle>Pangea Network</SiteTitle>
          <SubTitle>Admin Panel</SubTitle>
      </TitlesDiv>
    );
  }
}

export default Titles;