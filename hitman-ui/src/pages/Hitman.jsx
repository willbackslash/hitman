import React, {
  useEffect,
  useState,
} from 'react';

import useAxios from 'axios-hooks';
import PropTypes from 'prop-types';
import {
  Alert,
  Button,
  Col,
  Container,
  Form,
  Row,
} from 'react-bootstrap';
import { useParams } from 'react-router-dom';

import Loader from '../components/Loader';

const Hitman = () => {
  const { hitmanId } = useParams();
  const [{ data: hitman, loading, error }, getHitmanDetail] = useAxios({ url: `/users/${hitmanId}`, method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } });
  const [{ data: hitmen }] = useAxios({ url: '/users', method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } });
  const [managedHitmen, setManagedHitmen] = useState([]);

  useEffect(() => {
    getHitmanDetail();
  }, [hitmanId, getHitmanDetail]);

  useEffect(() => {
    if (hitman && hitman.managed_users) {
      setManagedHitmen(Array.from(hitman.managed_users, (hm) => hm.email));
    }
  }, [hitman]);

  return (
    <Container>
      <Row>
        <Col>
          <h1>Hitman detail</h1>
        </Col>
      </Row>
      <br />
      <Row>
        {(loading) && <Loader />}
        <Col xs="12">
          {error ? <Alert variant="danger">Error getting hitman detail, try again</Alert> : null}
        </Col>
        {hitman
            && (
            <Col xs={{ span: 8, offset: 2 }}>
              <Form>
                <Form.Group>
                  <Form.Label>Hitman id</Form.Label>
                  <Form.Control plaintext type="text" defaultValue={hitman.id} />
                </Form.Group>
                <Form.Group>
                  <Form.Label>First name</Form.Label>
                  <Form.Control plaintext type="text" defaultValue={hitman.first_name} />
                </Form.Group>
                <Form.Group>
                  <Form.Label>Last name</Form.Label>
                  <Form.Control plaintext type="text" defaultValue={hitman.last_name} />
                </Form.Group>
                <Form.Group>
                  <Form.Label>Email</Form.Label>
                  <Form.Control plaintext type="text" defaultValue={hitman.email} />
                </Form.Group>
                <Form.Group controlId="exampleForm.ControlSelect1">
                  <Form.Label>Status</Form.Label>
                  <Form.Control as="select">
                    <option selected>Activo</option>
                    <option>Inactivo</option>
                  </Form.Control>
                </Form.Group>
                {hitmen && (
                <Form.Group controlId="exampleForm.ControlSelect2">
                  <Form.Label>Managed hitmen</Form.Label>
                  <Form.Control as="select" multiple>
                    {hitmen.map((option) => (
                      <option
                        selected={managedHitmen.includes(option.email)}
                      >
                        {option.email}
                      </option>
                    ))}
                  </Form.Control>
                </Form.Group>
                ) }
                <Button disabled={loading} variant="primary" type="submit">
                  {!loading ? 'Save changes' : 'Saving ...'}
                </Button>
              </Form>
            </Col>
            )}
      </Row>
    </Container>
  );
};

Hitman.propTypes = {
  profile: PropTypes.shape({
    email: PropTypes.string,
  }).isRequired,
};

export default Hitman;
