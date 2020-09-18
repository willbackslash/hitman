import React from 'react';

import useAxios from 'axios-hooks';
import PropTypes from 'prop-types';
import {
  Alert,
  Badge,
  Col,
  Container,
  Row,
  Table,
} from 'react-bootstrap';
import { Link } from 'react-router-dom';

const Hitmen = ({ profile }) => {
  const [{ data, loading, error }] = useAxios({ url: '/users', method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } });

  const getPillColor = (isActive) => {
    if (!isActive) return 'danger';
    return 'success';
  };

  return (
    <Container>
      <Row>
        <Col>
          <h1>Hitmen</h1>
        </Col>
      </Row>
      <br />
      <Row>
        <Col>
          {error ? <Alert variant="danger">Error getting hitmen, try again</Alert> : null}
        </Col>
        {!loading
          && (
          <Col xs="12">
            <Table striped bordered hover size="sm" responsive>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Email</th>
                  <th>First name</th>
                  <th>Last name</th>
                  <th>Status</th>
                  <th>Date joined</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {(data && profile) && data.map((hitman) => (
                  <tr>
                    <td>{hitman.id}</td>
                    <td>{hitman.email}</td>
                    <td>{hitman.first_name}</td>
                    <td>{hitman.last_name}</td>
                    <td>
                      <Badge pill variant={getPillColor(hitman.is_active)}>
                        {hitman.is_active ? 'Active' : 'Inactive'}
                      </Badge>
                    </td>
                    <td>{hitman.date_joined}</td>
                    <td>
                      <Link to={`/hitmen/${hitman.id}`}>Detail</Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </Col>
          )}
      </Row>
    </Container>
  );
};

Hitmen.propTypes = {
  profile: PropTypes.shape({
    email: PropTypes.string,
  }).isRequired,
};

export default Hitmen;
