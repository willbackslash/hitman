import React, { useEffect } from 'react';

import useAxios from 'axios-hooks';
import { Formik } from 'formik';
import {
  Alert,
  Button,
  Col,
  Container,
  Form,
  Row,
} from 'react-bootstrap';
import {
  Link,
  useHistory,
} from 'react-router-dom';
import * as yup from 'yup';

const schema = yup.object({
  first_name: yup.string().required(),
  last_name: yup.string().required(),
  email: yup.string().required(),
  password: yup.string().matches(/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/).required(),
});

const Signup = () => {
  const history = useHistory();
  const [{ data, loading, error }, callRegisterService] = useAxios({ url: '/users', method: 'POST' }, { manual: true });
  const register = (formData) => {
    callRegisterService({ data: formData });
  };

  useEffect(() => {
    if (data && data.token) {
      sessionStorage.setItem('SESSION_AUTH', data.token);
      history.push('/hits');
      window.location.reload();
    }
  }, [data, history]);

  return (
    <Formik
      validationSchema={schema}
      onSubmit={register}
      initialValues={{
        email: '',
        password: '',
      }}
    >
      {({
        handleSubmit,
        handleChange,
        values,
        errors,
      }) => (
        <Container>
          <Row className="vertical-center">
            <Col md={{ span: 4, offset: 4 }}>
              <h1>Sign Up to Hitman</h1>
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              <Form onSubmit={handleSubmit}>
                <Form.Group>
                  <Form.Label>First name</Form.Label>
                  <Form.Control
                    id="first_name"
                    type="first_name"
                    placeholder="Enter your name ..."
                    value={values.first_name}
                    onChange={handleChange}
                    isInvalid={!!errors.first_name}
                  />
                </Form.Group>
                <Form.Group>
                  <Form.Label>Last name</Form.Label>
                  <Form.Control
                    id="last_name"
                    type="last_name"
                    placeholder="Enter your last name ..."
                    value={values.last_name}
                    onChange={handleChange}
                    isInvalid={!!errors.last_name}
                  />
                </Form.Group>
                <Form.Group>
                  <Form.Label>Email address</Form.Label>
                  <Form.Control
                    id="email"
                    type="email"
                    placeholder="Enter email"
                    value={values.email}
                    onChange={handleChange}
                    isInvalid={!!errors.email}
                  />
                </Form.Group>
                <Form.Group>
                  <Form.Label>Password</Form.Label>
                  <Form.Control
                    id="password"
                    type="password"
                    placeholder="Password"
                    value={values.password}
                    onChange={handleChange}
                    isInvalid={!!errors.password}
                  />
                  <Form.Text className="text-muted">
                    Minimum eight characters, at least one letter and one number
                  </Form.Text>
                </Form.Group>
                <Button disabled={loading} variant="primary" type="submit">
                  {!loading ? 'Sign up' : 'Registering ...'}
                </Button>
              </Form>
              <span>
                <br />
              </span>
              {error ? (
                <Alert variant="danger">
                  Could not register:
                  {' '}
                  {error.response.data.detail}
                </Alert>
              ) : null}
              {data ? (
                <Alert variant="success">
                  The account was created:
                  {' '}
                  <Link to="/">Go to Login</Link>
                </Alert>
              ) : null}
            </Col>
          </Row>
        </Container>
      )}
    </Formik>
  );
};
export default Signup;
