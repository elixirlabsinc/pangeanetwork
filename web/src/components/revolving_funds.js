import axios from 'axios';
import React, { Component } from 'react';
import styled from 'styled-components';

const ContentDiv = styled.div`
  background-color: #F6F9FC;
  padding-top: 50px;
  min-height: 80vh;
`;

const ContentArea = styled.div`
  margin: auto;
  width: 80%;
  padding: 12px;
`;

const CoopTable = styled.div`
  width: 100%;
  display: inline-grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr;
  grid-template-rows: auto;
`;

const CoopField = styled.div`
  background-color: #FFFFFF;
  padding: 12px;
  margin: 2px;
  font-family: Comfortaa;
  font-size: 12px;
  line-height: 14px;
  vertical-align: middle;
`;

const HeaderField = styled.div`
  padding: 12px;
  margin: 2px;
  font-family: Comfortaa;
  line-height: 14px;
  vertical-align: middle;
  font-style: normal;
  font-weight: normal;
  font-size: 14px;
  line-height: 14px;
  letter-spacing: 0.14em;
  color: #262164;
`;

class RevolvingFunds extends Component {
  state = {
    data: [],
  };

  componentDidMount() {
    console.log('fetching revolving_funds')
    axios.get('http://localhost:5002/revolving_funds')
    .then(results => {
      this.setState({data: results.data.revolving_funds});
    })
  }

  render() {
    return (
      <ContentDiv>
        <ContentArea>
          <CoopTable key='header'>
            <HeaderField>User</HeaderField>
            <HeaderField>Initial Balance</HeaderField>
            <HeaderField>Current Balance</HeaderField>
          </CoopTable>
            {this.state.data.map(({id, user, initial_balance, balance}) => {
              return (
                <CoopTable key={id}>
                  <CoopField>{user}</CoopField>
                  <CoopField>{initial_balance}</CoopField>
                  <CoopField>{balance}</CoopField>
                </CoopTable>
              )
            })}
        </ContentArea>
      </ContentDiv>
    );
  }
}

export default RevolvingFunds;
