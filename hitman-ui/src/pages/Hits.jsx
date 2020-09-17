import React, { useEffect } from 'react';

import useAxios from 'axios-hooks';
import PropTypes from 'prop-types';
import {
  Alert,
  Button,
  ButtonGroup,
  Col,
  Container,
  Dropdown,
  DropdownButton,
  Row,
  Table,
} from 'react-bootstrap';

import Loader from '../components/Loader';

const Hits = ({ profile }) => {
  const [{ data, loading, error }, callGetService] = useAxios({ url: '/hits', method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } });
  const [{ data: updatedSuccessfully, loading: updating, error: errorUpdating }, callUpdateHitService] = useAxios({ method: 'PUT', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } }, { manual: true });

  const markAsCompleted = (hitId) => {
    callUpdateHitService({ url: `/hits/${hitId}`, data: { status: 'COMPLETED' } });
  };

  const markAsFailed = (hitId) => {
    callUpdateHitService({ url: `/hits/${hitId}`, data: { status: 'FAILED' } });
  };

  useEffect(() => {
    if (updatedSuccessfully) {
      callGetService();
    }
  }, [updatedSuccessfully, callGetService]);

  return (
    <Container>
      <Row>
        <Col>
          <h1>My Hits</h1>
        </Col>
      </Row>
      <Row>
        <Col>
          <Button>Add a hit</Button>
        </Col>
      </Row>
      <br />
      <Row>
        {(loading || updating) && <Loader />}
        <Col>
          {error ? <Alert variant="danger">Error getting hits, try again</Alert> : null}
          {errorUpdating ? <Alert variant="danger">Sorry we couldn&apos;t update the hit</Alert> : null}
          {updatedSuccessfully && <Alert variant="success">Hit updated successfully</Alert>}
        </Col>
        {!loading
        && (
        <Col>
          <Table striped bordered hover size="sm" responsive>
            <thead>
              <tr>
                <th>#</th>
                <th>Requester</th>
                <th>Assigned to</th>
                <th>Target</th>
                <th>Description</th>
                <th>Status</th>
                <th>Created</th>
                <th>Last update</th>
              </tr>
            </thead>
            <tbody>
              {(data && profile) && data.map((hit) => (
                <tr>
                  <td>{hit.id}</td>
                  <td>{hit.requester.email}</td>
                  <td>{hit.assigned_to.email}</td>
                  <td>{hit.target_name}</td>
                  <td>{hit.description}</td>
                  <td>
                    { hit.assigned_to.email === profile.email && hit.status === 'ASSIGNED'
                      ? (
                        <DropdownButton
                          as={ButtonGroup}
                          key="primary"
                          variant="primary"
                          title={hit.status}
                        >
                          <Dropdown.Item
                            onClick={() => markAsFailed(hit.id)}
                          >
                            Failed
                          </Dropdown.Item>
                          <Dropdown.Item
                            onClick={() => markAsCompleted(hit.id)}
                          >
                            Completed
                          </Dropdown.Item>
                        </DropdownButton>
                      ) : `${hit.status}`}
                  </td>
                  <td>{hit.created_at}</td>
                  <td>{hit.updated_at}</td>
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

Hits.propTypes = {
  profile: PropTypes.shape({
    email: PropTypes.string,
  }).isRequired,
};

export default Hits;
