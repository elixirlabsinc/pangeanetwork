const loginMode = (state = 'login', action) => {
  switch (action.type) {
    case 'SET_TO_LOGIN_MODE':
      return 'login';
    default:
      return state;
  }
};

// loginMode will be on the redux state at:
// state.loginMode
export default loginMode;
