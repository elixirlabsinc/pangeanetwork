import React from 'react';
import PropTypes from 'prop-types';
import DropDown from 'react-dd-menu';
import { FaAngleDown } from 'react-icons/fa';

class DropDownList extends React.Component {
  state = {
    isOpen: false,
  };

  toggle = () => {
    this.setState(({ isOpen }) => ({
      isOpen: !isOpen,
    }));
  };

  close = () => {
    this.setState({ isOpen: false });
  };

  render() {
    const { value, onSelect, items, placeholder } = this.props;
    const label = value ? items.find(item => { return item.id === value; }).name : ''

    return (
      <DropDown
        isOpen={this.state.isOpen}
        close={this.close}
        animate={false}
        enterTimeout={10}
        leaveTimeout={10}
        closeOnInsideClick
        toggle={
          <div>
            <button
              key={placeholder}
              type="button"
              className='btn btn-default dropdown'
              onClick={this.toggle}
              aria-expanded={this.state.isOpen}
            >
              { label ?
                <span>{label}</span>
                :
                <span className='placeholder'>
                  {placeholder}
                </span>
              }
              {}
              <FaAngleDown style={{ float: 'right', marginTop: '3px', marginLeft: '2px', width: '0.5em' }} />
            </button>
          </div>
        }
        align="left"
      >
        {items.map(item => (
          <li key={item.id}>
            <button
              key={item.id}
              type="button"
              onClick={() => onSelect(item.id)}
            >
              {item.name}
            </button>
          </li>
        ))}
      </DropDown>
    );
  }
}

DropDownList.propTypes = {
  onSelect: PropTypes.func.isRequired,
  value: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number
  ]),
  items: PropTypes.array,
  placeholder: PropTypes.string,
};

DropDownList.defaultProps = {
  value: '',
  items: [],
  placeholder: 'Select an Item'
}

export default DropDownList;

