import React, {
  useEffect,
  useState,
} from 'react';

import useAxios from 'axios-hooks';
import PropTypes from 'prop-types';
import {
  Alert,
  Badge,
  Button,
  Col,
  Container,
  Form,
  Row,
} from 'react-bootstrap';
import {
  Link,
  useParams,
} from 'react-router-dom';

import Loader from '../components/Loader';
import {
  isBoss,
  isHitman,
  isManager,
} from '../utils';

const Hitman = ({ profile }) => {
  const { hitmanId } = useParams();
  const [{ data: updatedCorrectly, loading: updating, error: errorUpdating }, callUpdateHitmanService] = useAxios({ url: `/users/${hitmanId}`, method: 'PUT', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } }, { manual: true });
  const [{ data: hitman, loading, error }, callHitmanService] = useAxios({ url: `/users/${hitmanId}`, method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } }, { manual: true });
  const [{ data: hitmen }] = useAxios({ url: '/users', method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } });
  const [managedHitmen, setManagedHitmen] = useState([]);
  const [newStatus, setNewStatus] = useState(null);
  const [newManagedUsers, setnewManagedUsers] = useState(null);

  const handleSubmit = async () => {
    await callUpdateHitmanService({ method: 'PUT', data: { is_active: newStatus, managed_users: newManagedUsers } });
  };

  const handleStatusChange = (e) => {
    setNewStatus(e.target.value === 'active');
  };

  const handleManagedUsersChange = (e) => {
    setnewManagedUsers(Array.from(e.target.selectedOptions, (option) => ({ id: option.value })));
  };

  useEffect(() => {
    callHitmanService();
  }, [hitmanId, updatedCorrectly, callHitmanService]);

  useEffect(() => {
    if (hitman) {
      setNewStatus(hitman.is_active);
      setnewManagedUsers(hitman.managed_users);
    }
  }, [hitman]);

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
        {(loading || updating) && <Loader />}
        <Col xs="12">
          {updatedCorrectly ? (
            <Alert variant="success">
              Updated correctly
              {' '}
              <Link to="/hitmen">Go to hitmen list</Link>
            </Alert>
          ) : null}
          {errorUpdating ? (
            <Alert variant="danger">
              Error updating:
              {' '}
              { errorUpdating.response.data.detail }
            </Alert>
          ) : null}
          {error ? <Alert variant="danger">Error getting hitman detail, try again</Alert> : null}
        </Col>
        {hitman
            && (
            <Col xs={{ span: 8, offset: 2 }}>
              <Form onSubmit={(e) => e.preventDefault()}>
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
                  <Form.Control as="select" onChange={handleStatusChange}>
                    <option value="active" selected={hitman.is_active}>Activo</option>
                    <option value="inactive" selected={!hitman.is_active}>Inactivo</option>
                  </Form.Control>
                </Form.Group>
                <Form.Group>
                  <Form.Label>Role</Form.Label>
                  {' '}
                  <>
                    { isHitman(hitman) && (
                    <Badge pill variant="primary">
                      Hitman
                    </Badge>
                    )}
                    { isManager(hitman) && (
                      <Badge pill variant="warning">
                        Manager
                      </Badge>
                    )}
                    { isBoss(hitman) && (
                      <Badge pill variant="danger">
                        Boss
                      </Badge>
                    )}
                  </>
                </Form.Group>
                {(hitmen && isBoss(profile)) && (
                <Form.Group controlId="exampleForm.ControlSelect2">
                  <Form.Label>Managed hitmen</Form.Label>
                  <Form.Control as="select" multiple onChange={handleManagedUsersChange}>
                    {hitmen.filter((user) => isHitman(user)).map((option) => (
                      <option
                        value={option.id}
                        selected={managedHitmen.includes(option.email)}
                      >
                        {option.email}
                      </option>
                    ))}
                  </Form.Control>
                </Form.Group>
                ) }
                <Button onClick={handleSubmit} disabled={loading || (newStatus == null && newManagedUsers == null)} variant="primary" type="submit">
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
