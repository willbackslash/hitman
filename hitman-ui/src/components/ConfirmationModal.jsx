import React from 'react';

import PropTypes from 'prop-types';
import {
  Button,
  Modal,
} from 'react-bootstrap';

const ConfirmationModal = ({
  show, setShow, onConfirm, onConfirmParams,
}) => {
  const handleConfirm = () => {
    onConfirm.action(onConfirmParams);
    setShow(false);
  };
  return (
    <Modal show={show}>
      <Modal.Header>
        <Modal.Title>Are you sure?</Modal.Title>
      </Modal.Header>

      <Modal.Body>
        <p>This action can not be undone</p>
      </Modal.Body>

      <Modal.Footer>
        <Button variant="secondary" onClick={() => setShow(false)}>Close</Button>
        <Button variant="primary" onClick={() => handleConfirm()}>Save changes</Button>
      </Modal.Footer>
    </Modal>
  );
};

ConfirmationModal.defaultProps = {
  onConfirmParams: {},
};

ConfirmationModal.propTypes = {
  show: PropTypes.bool.isRequired,
  setShow: PropTypes.func.isRequired,
  onConfirm: PropTypes.func.isRequired,
  onConfirmParams: PropTypes.oneOfType(Object),
};

export default ConfirmationModal;
