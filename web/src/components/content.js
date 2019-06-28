import React, { Component } from 'react';

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
    .then(data => {
      this.setState({data: data.results});
    })
  }
  
  render() {
    return (
      <React.Fragment>
        <p>Content</p>
        <div>
          {this.state.data.map(({name, age, city}) => {
            return (
              <p>name: {name}, age: {age}, city: {city}</p>
            )
          })}
        </div>
      </React.Fragment>
    );
  }
}

export default Content;