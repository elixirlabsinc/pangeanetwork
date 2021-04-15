import React, { Component } from 'react';
import axios from 'axios';
import DropDownList from '../dropdown/DropDownList';
import styled from 'styled-components';

const ContentDiv = styled.div`
  background-color: #F6F9FC;
  font-family: Questrial;
`;

const ContentArea = styled.div`
  margin: auto;
  width: 80%;
  padding: 12px;
`;

const FormTitle = styled.div`
  font-size: 36px;
  line-height: 37px;
  color: #7870DC;
  text-align: center;
  padding-top: 100px;
  font-weight: 500;
`;

const FormRow = styled.div`
  padding: 25px;
  margin: auto;
  width: 1000px
`;

const FormLabel = styled.div`
  font-size: 22px;
  line-height: 37px;
  color: #7870DC;
  letter-spacing: 0.14em;
  font-weight: 500;
`;

const FormInput = styled.input`
  width: 400px !important;
  border: 0px !important;
  border-radius: 0px !important;
`;

const ActionButtons = styled.div`
  padding: 50px;
  text-align: center;
`;

class MembersForm extends Component {
  state = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    co_op_id: '',
    role_id: '',
    roles: [],
    coops: []
  };

  componentDidMount = () => {
    axios.get('http://localhost:5000/roles')
    .then(results => {
      this.setState({roles: results.data.data});
    })
    axios.get('http://localhost:5000/coops')
    .then(results => {
      this.setState({coops: results.data.data});
    })
  }

  handleChange = (changedState) => {
    this.setState(changedState);
  }

  submitForm = () => {
    const payload = {
      first_name: this.state.first_name,
      last_name: this.state.last_name,
      email: this.state.email,
      phone: this.state.phone,
      co_op_id: this.state.co_op_id,
      role_id: this.state.role_id
    }
    axios.post('http://localhost:5000/members', payload)
      .then(result => {
        console.log(result);
        if (result.status === 200) {
          window.location.assign('/members')
        }
        }
      )
  }

  render() {
    return (
      <ContentDiv>
        <ContentArea>
          <FormTitle>New User</FormTitle>
          <div>
            <FormRow>
              <div className='row'>
                <div className='col-md-6'>
                  <FormLabel>First Name</FormLabel>
                  <FormInput value={this.state.first_name} onChange={(event) => this.handleChange({first_name: event.target.value})} className='form-control'></FormInput>
                </div>
                <div className='col-md-6'>
                  <FormLabel>Last Name</FormLabel>
                  <FormInput value={this.state.last_name} onChange={(event) => this.handleChange({last_name: event.target.value})} className='form-control'></FormInput>
                </div>
              </div>
            </FormRow>
            <FormRow>
              <div className='row'>
                <div className='col-md-6'>
                  <FormLabel>Email</FormLabel>
                  <FormInput value={this.state.email} onChange={(event) => this.handleChange({email: event.target.value})} className='form-control'></FormInput>
                </div>
                <div className='col-md-6'>
                  <FormLabel>Phone</FormLabel>
                  <FormInput value={this.state.phone} onChange={(event) => this.handleChange({phone: event.target.value})} className='form-control'></FormInput>
                </div>
              </div>
            </FormRow>
            <FormRow>
              <div className='row'>
                <div className='col-md-6'>
                  <FormLabel>Co-op</FormLabel>
                  <DropDownList 
                    onSelect={newCoOp => this.handleChange({co_op_id: newCoOp})}
                    value={this.state.co_op_id}
                    items={this.state.coops}
                    placeholder='Co-Op'
                  />
                </div>
                <div className='col-md-6'>
                  <FormLabel>Role</FormLabel>
                  <DropDownList 
                    onSelect={newRole => this.handleChange({role_id: newRole})}
                    value={this.state.role_id}
                    items={this.state.roles}
                    placeholder='Role'
                  />
                </div>
              </div>
            </FormRow>
          </div>
          <ActionButtons>
            <button onClick={() => this.submitForm()} className='btn btn-primary'>Submit</button>
            <br /><br />
            <button onClick={() => window.location.assign('/members')} className='btn btn-link'>Cancel</button>
          </ActionButtons>
        </ContentArea>
      </ContentDiv>
    );
  }
}

export default MembersForm;