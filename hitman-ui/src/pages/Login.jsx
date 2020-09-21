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
  email: yup.string().required(),
  password: yup.string().required(),
});

const Login = () => {
  const history = useHistory();
  const [{ data, loading, error }, callAuthService] = useAxios({ url: '/auth/token', method: 'POST' }, { manual: true });
  const authenticate = ({ email, password }) => {
    callAuthService({ url: '/auth/token', method: 'POST', data: { username: email, password } });
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
      onSubmit={authenticate}
      initialValues={{
        email: '',
        password: '',
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
        // TODO: Refactor in multiple files and remove password restriction
        <Container>
          <Row className="vertical-center">
            <Col md={{ span: 4, offset: 4 }}>
              <h1>Welcome to Hitman</h1>
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              <Form onSubmit={handleSubmit}>
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
                  {!loading ? 'Sign in' : 'Authenticating ...'}
                </Button>
              </Form>
              <span>
                <br />
              </span>
              {error ? <Alert variant="danger">Invalid credentials</Alert> : null}
              {data ? <Alert variant="success">{data.token}</Alert> : null}
            </Col>
            <Col md={{ span: 4, offset: 4 }}>
              Don&apos;t have an account?
              {' '}
              <Link to="/register">Sign Up</Link>
            </Col>
          </Row>
        </Container>
      )}
    </Formik>
  );
};
export default Login;
