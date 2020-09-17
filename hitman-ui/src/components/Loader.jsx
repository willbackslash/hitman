import React from 'react';
import { Col } from 'react-bootstrap';
import spinner from '../assets/hitman_spinner.gif';

const Loader = () => (
  <Col xs="12">
    <img src={spinner} alt="spinner" height="80px" width="auto" style={{ margin: 'auto' }} />
  </Col>
);

export default Loader;
