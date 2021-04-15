import React, { Component } from 'react';
import axios from 'axios';
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

const NewButton = styled.a`
  background: #262164;
  box-shadow: 0px 4px 4px rgb(0 0 0 / 25%);
  text-decoration: none;
  color: white;
  border-radius: 50%;
  padding: 0px 20px 5px 20px;
  font-size: 40px;
  position: fixed;
  right: 75px;
  top: 250px;
  :hover {
    text-decoration: none;
    color: white;
  }
`

class Members extends Component {
  state = {
    data: [],
  };

  componentDidMount() {
    axios.get('http://localhost:5000/members')
    .then(results => {
      this.setState({data: results.data.data});
    })
  }

  render() {
    return (
      <ContentDiv>
        <ContentArea>
          <NewButton href="/members/new">+</NewButton>
          <CoopTable key='header'>
            <HeaderField>Name</HeaderField>
            <HeaderField>Co-Op</HeaderField>
            <HeaderField>Phone</HeaderField>
            <HeaderField>Role</HeaderField>
            <HeaderField>Loan Balance</HeaderField>
          </CoopTable>
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

export default Members;