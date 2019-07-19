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
  grid-template-columns: 2fr 1fr 2fr 1fr 1fr;
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

class Content extends Component {
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
            {this.state.data.map(({name, coop, phone, role, loan_balance}) => {
              return (
                <CoopTable key={name}>
                  <CoopField>{name}</CoopField>
                  <CoopField>{coop}</CoopField>
                  <CoopField>{phone}</CoopField>
                  <CoopField>{role}</CoopField>
                  <CoopField>{loan_balance}</CoopField>
                </CoopTable>
              )
            })}
        </ContentArea>
      </ContentDiv>
    );
  }
}

export default Content;