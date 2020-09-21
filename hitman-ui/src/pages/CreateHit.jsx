import React from 'react';

import useAxios from 'axios-hooks';
import { Formik } from 'formik';
import PropTypes from 'prop-types';
import {
  Alert,
  Button,
  Col,
  Container,
  Form,
  Row,
} from 'react-bootstrap';
import { Link } from 'react-router-dom';
import * as yup from 'yup';

import Loader from '../components/Loader';
import {
  isBoss,
  isHitman,
} from '../utils';

const Hitman = ({ profile }) => {
  const schema = yup.object({
    description: yup.string().required(),
    target_name: yup.string().required(),
    assigned_to: yup.string().required(),
  });
  const [{ data: hitmen, loading, error }] = useAxios({ url: '/users', method: 'GET', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } });
  const [{ data: createdHit, loading: creatingHit, error: errorCreating }, callCreateHitService] = useAxios({ url: '/hits', method: 'POST', headers: { Authorization: `Token ${sessionStorage.getItem('SESSION_AUTH')}` } }, { manual: true });
  const createHit = (formData) => {
    callCreateHitService({ data: formData });
  };
  return (
    <Container>
      <Row>
        <Col>
          <h1>Create a Hit</h1>
        </Col>
      </Row>
      <br />
      <Row>
        {(loading || creatingHit) && <Loader />}
        <Col xs="12">
          {createdHit ? (
            <Alert variant="success">
              Hit created correctly
              {' '}
              <Link to="/hits">Go to hits list</Link>
            </Alert>
          ) : null}
          {errorCreating ? (
            <Alert variant="danger">
              Error creating hit:
              {' '}
              { errorCreating.response.data.detail }
            </Alert>
          ) : null}
          {error ? <Alert variant="danger">Error getting hitmen list, try again</Alert> : null}
        </Col>
        {hitmen
              && (
              <Col xs={{ span: 8, offset: 2 }}>
                <Formik
                  validationSchema={schema}
                  onSubmit={createHit}
                  initialValues={{
                    description: '',
                    target_name: '',
                    assigned_to: '',
                  }}
                >
                  {({
                    handleSubmit,
                    handleChange,
                    // handleBlur,
                    values,
                    // touched,
                    // isValid,
                    errors,
                  }) => (
                    <Form onSubmit={handleSubmit}>
                      <Form.Group>
                        <Form.Label>Target name</Form.Label>
                        <Form.Control
                          id="target_name"
                          type="text"
                          value={values.target_name}
                          onChange={handleChange}
                          isInvalid={!!errors.target_name}
                        />
                      </Form.Group>
                      <Form.Group>
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                          id="description"
                          as="textarea"
                          rows={3}
                          value={values.description}
                          onChange={handleChange}
                          isInvalid={!!errors.description}
                        />
                      </Form.Group>
                      <Form.Group>
                        <Form.Label>Assign to</Form.Label>
                        <Form.Control
                          id="assigned_to"
                          as="select"
                          value={values.assigned_to}
                          onChange={handleChange}
                          isInvalid={!!errors.assigned_to}
                        >
                          <option>-- Select a hitman --</option>
                          {hitmen.filter((user) => (
                            (isBoss(profile)
                              || isHitman(user)
                            ) && profile.email !== user.email)).map((option) => (
                              <option
                                value={option.email}
                                selected={option.email === values.assigned_to}
                              >
                                {option.first_name}
                                {' '}
                                {option.last_name}
                                {' - '}
                                {option.email}
                              </option>
                          ))}
                        </Form.Control>
                      </Form.Group>
                      <Button disabled={false} variant="primary" type="submit">
                        {!loading ? 'Save changes' : 'Saving ...'}
                      </Button>
                    </Form>
                  )}
                </Formik>
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
