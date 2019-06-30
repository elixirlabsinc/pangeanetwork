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
          <p>Content</p>
          <div>
            {this.state.data.map(({name, age, city}) => {
              return (
                <p key={name}>name: {name}, age: {age}, city: {city}</p>
              )
            })}
          </div>
        </ContentArea>
      </ContentDiv>
    );
  }
}

export default Content;