import React, { Component } from 'react';
import { connect } from 'react-redux';
import { TextField, Button } from '@material-ui/core';
import styled from 'styled-components';

const ContentDiv = styled.div`
  background-color: #F6F9FC;
`;

const ContentArea = styled.div`
  margin: auto;
  width: 80%;
  padding: 12px;
`;

class Login extends Component {
  state = {
    username: '',
    password: '',
  };

  login = (event) => {
    event.preventDefault();

    if (this.state.username && this.state.password) {
      this.props.dispatch({
        type: 'LOGIN',
        payload: {
          username: this.state.username,
          password: this.state.password,
        },
      });
    } else {
      this.props.dispatch({ type: 'LOGIN_INPUT_ERROR' });
    }
  } // end login

  handleInputChangeFor = propertyName => (event) => {
    this.setState({
      [propertyName]: event.target.value,
    });
  }

  render() {
    return (
      <div>

        {/* error messages */}
        {this.props.errors.loginMessage && (
          <h2
            className="alert"
            role="alert"
          >
            {this.props.errors.loginMessage}
          </h2>
        )}
        <ContentDiv>
          <ContentArea>
          
            <center>
            {/* log in form */}
            <form id="loginForm" onSubmit={this.login}>
              
              <h2>log in</h2>

              <TextField
                required
                autoFocus
                className="textField"
                value={this.state.username}
                type="text"
                label="email address"
                variant="outlined"
                margin="normal"
                onChange={this.handleInputChangeFor('username')} />

              <br />

              <TextField
                required
                className="textField"
                value={this.state.password}
                type="password"
                label="password"
                variant="outlined"
                margin="normal"
                onChange={this.handleInputChangeFor('password')} />

              <br /><br />

              <Button className="form-button" type="submit" variant="contained" color="primary">
                log in
              </Button>

            </form>
            </center>

          </ContentArea>
        </ContentDiv>
      </div>
    );
  }
}

// Instead of taking everything from state, we just want the error messages.
// if you wanted you could write this code like this:
// const mapStateToProps = ({errors}) => ({ errors });
const mapStateToProps = state => ({
  errors: state.errors,
});

export default connect(mapStateToProps)(Login);