import React from 'react';
import { useHistory } from 'react-router-dom';

const Logout = () => {
  const history = useHistory();
  sessionStorage.removeItem('SESSION_AUTH');
  history.push('/');
  return (<h2>Redirecting...</h2>);
};

export default Logout;
