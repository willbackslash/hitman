import React from 'react';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
// eslint-disable-next-line no-unused-vars
import axios from './config/axios';
import MainRouter from './router';

function App() {
  return (
    <MainRouter />
  );
}

export default App;
