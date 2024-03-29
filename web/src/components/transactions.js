import React, { Component } from 'react';
import styled from 'styled-components';

const ContentDiv = styled.div`
  background-color: #F6F9FC;
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

class Transactions extends Component {
  constructor() {
    super();
    this.state = {
      data: [],
    };
  }

  componentDidMount() {
    fetch('http://localhost:5000/transactions')
    .then(results => {
      return results.json();
    })
    .then(results => {
      this.setState({data: results.data});
    })
  }

  render() {
    return (
      <ContentDiv>
        <ContentArea>
          <CoopTable key='header'>
            <HeaderField>Member</HeaderField>
            <HeaderField>Amount</HeaderField>
            <HeaderField>Previous Balance</HeaderField>
            <HeaderField>New Balance</HeaderField>
            <HeaderField>Status</HeaderField>
            <HeaderField>Timestamp</HeaderField>
          </CoopTable>
            {this.state.data.map(({user_name, amount, previous_balance, new_balance, state, timestamp}) => {
              return (
                <CoopTable key={timestamp}>
                  <CoopField>{user_name}</CoopField>
                  <CoopField>{amount}</CoopField>
                  <CoopField>{previous_balance}</CoopField>
                  <CoopField>{new_balance}</CoopField>
                  <CoopField>{state}</CoopField>
                  <CoopField>{timestamp}</CoopField>
                </CoopTable>
              )
            })}
        </ContentArea>
      </ContentDiv>
    );
  }
}

export default Transactions;