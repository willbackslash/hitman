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
  ButtonGroup,
  Col,
  Container,
  Dropdown,
  DropdownButton,
  Row,
  Table,
} from 'react-bootstrap';

import ConfirmationModal from '../components/ConfirmationModal';
import Loader from '../components/Loader';
import {
  canAssignHits,
  isBoss,
  isManager,
} from '../utils';

const Hits = ({ profile }) => {
  const [showConfirmationModal, setShowConfirmationModal] = useState(false);
  const [modalAction, setModalAction] = useState(() => null);
  const [modalActionParams, setModalActionParams] = useState(null);
  const [{ data, loading, error }, callGetService] = useAxios({ url: '/hits', method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } });
  const [{ data: updatedSuccessfully, loading: updating, error: errorUpdating }, callUpdateHitService] = useAxios({ method: 'PUT', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } }, { manual: true });
  const [{ data: hitmen, loading: loadingHitmen, error: errorGettingHitmen }, getHitmenList] = useAxios({ url: '/users', method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } }, { manual: true });

  const markAsCompleted = (hitId) => {
    setModalAction({ action: callUpdateHitService });
    setModalActionParams({ url: `/hits/${hitId}`, data: { status: 'COMPLETED' } });
    setShowConfirmationModal(true);
  };

  const markAsFailed = (hitId) => {
    setModalAction({ action: callUpdateHitService });
    setModalActionParams({ url: `/hits/${hitId}`, data: { status: 'FAILED' } });
    setShowConfirmationModal(true);
  };

  const assignHit = (hitId, assignToEmail) => {
    callUpdateHitService({ url: `/hits/${hitId}`, data: { assigned_to: assignToEmail } });
  };

  useEffect(() => {
    if (updatedSuccessfully) {
      callGetService();
    }
  }, [updatedSuccessfully, callGetService]);

  useEffect(() => {
    if (profile && data && (isBoss(profile) || isManager(profile))) {
      getHitmenList();
    }
  }, [profile, data, getHitmenList]);

  const getPillColor = (status) => {
    if (status === 'COMPLETED') return 'success'; // TODO: centralize hit status in constants file
    if (status === 'FAILED') return 'danger';
    return 'primary';
  };

  return (
    <Container>
      <ConfirmationModal
        show={showConfirmationModal}
        setShow={setShowConfirmationModal}
        onConfirm={modalAction}
        onConfirmParams={modalActionParams}
      />
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
        {(loading || updating || loadingHitmen) && <Loader />}
        <Col>
          {error ? <Alert variant="danger">Error getting hits, try again</Alert> : null}
          {errorUpdating ? (
            <Alert variant="danger">
              Sorry we couldn&apos;t update the hit:
              {errorUpdating.response.data.detail}
            </Alert>
          ) : null}
          {errorGettingHitmen ? (
            <Alert variant="danger">
              Sorry we couldn&apos;t get the hitmen list
            </Alert>
          ) : null}
          {updatedSuccessfully && <Alert variant="success">Hit updated successfully</Alert>}
        </Col>
        {!loading
        && (
        <Col xs="12">
          { data.length ? (
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
                    <td>
                      {canAssignHits(profile) && hitmen
                        ? (
                          <DropdownButton
                            as={ButtonGroup}
                            key="primary"
                            variant="primary"
                            title={hit.assigned_to.email}
                          >
                            {
                            hitmen.map((hitman) => (
                              <Dropdown.Item
                                onClick={() => assignHit(hit.id, hitman.email)}
                              >
                                {hitman.email}
                              </Dropdown.Item>
                            ))
                          }
                          </DropdownButton>
                        )
                        : `${hit.assigned_to.email}`}
                    </td>
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
                        ) : (
                          <Badge pill variant={getPillColor(hit.status)}>
                            {hit.status}
                          </Badge>
                        )}
                    </td>
                    <td>{new Date(hit.created_at).toLocaleString()}</td>
                    <td>{new Date(hit.updated_at).toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          ) : (<h2>No hits assigned to you yet, chill!</h2>)}
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
