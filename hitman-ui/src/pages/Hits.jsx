import React from 'react';
import {
  Container, Row, Col, Table, Button, DropdownButton, ButtonGroup, Dropdown,
} from 'react-bootstrap';

const Hits = () => (
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
    <Row>
      <Col>
        <Table striped bordered hover size="sm" responsive>
          <thead>
            <tr>
              <th>#</th>
              <th>Assigned to</th>
              <th>Description</th>
              <th>Target</th>
              <th>Status</th>
              <th>Created</th>
              <th>Last update</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>1</td>
              <td>Mark</td>
              <td>Its easy</td>
              <td>@Target</td>
              <td>
                <DropdownButton
                  as={ButtonGroup}
                  key="primary"
                  id="dropdown-variants-primary"
                  variant="primary"
                  title="primary"
                >
                  <Dropdown.Item eventKey="1">Action</Dropdown.Item>
                  <Dropdown.Item eventKey="2">Another action</Dropdown.Item>
                  <Dropdown.Item eventKey="3" active>
                    Active Item
                  </Dropdown.Item>
                  <Dropdown.Divider />
                  <Dropdown.Item eventKey="4">Separated link</Dropdown.Item>
                </DropdownButton>
              </td>
              <td>2020-01-01</td>
              <td>2020-01-01</td>
            </tr>
            <tr>
              <td>2</td>
              <td>Jacob</td>
              <td>Thornton</td>
              <td>@Target</td>
              <td>Completed</td>
              <td>2020-01-01</td>
              <td>2020-01-01</td>
            </tr>
            <tr>
              <td>3</td>
              <td>Issac</td>
              <td>new and fast</td>
              <td>@Target</td>
              <td>Failed</td>
              <td>2020-01-01</td>
              <td>2020-01-01</td>
            </tr>
          </tbody>
        </Table>
      </Col>
    </Row>
  </Container>
);

export default Hits;
