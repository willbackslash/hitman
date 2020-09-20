import React from 'react';

import {
  Col,
  Container,
  Row,
} from 'react-bootstrap';

const Page404 = () => (
  <Container>
    <Row>
      <Col xs="12" style={{ textAlign: 'center' }}>
        <h1>404: Target not found</h1>
      </Col>
    </Row>
  </Container>
);

export default Page404;
