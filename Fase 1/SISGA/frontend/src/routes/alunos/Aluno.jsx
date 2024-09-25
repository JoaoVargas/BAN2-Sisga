import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

import CustomNavbar from '../../components/CustomNavbar.jsx';
import { Button, Card, Container, Modal, Form } from 'react-bootstrap';

const Aluno = () => {
  const [showToast, setShowToast] = useState(false);
  const [messageToast, setMessageToast] = useState('');
  const [variantToast, setVariantToast] = useState('');

  const [aluno, setAluno] = useState([]);

  const [modalEditar, setModalEditar] = useState(false);
  const [modalExcluir, setModalExcluir] = useState(false);

  let { cod_aluno } = useParams();

  useEffect(() => {
    fetch('http://0.0.0.0:5002/alunospessoas/' + cod_aluno, { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then((res) => res.json())
    .then((dataAluno) => {
      console.log(dataAluno[0]);
      setAluno(dataAluno[0]);
    })
  }, []);

  const date = new Date(aluno[4]);
  const day = String(date.getUTCDate()).padStart(2, '0');
  const month = String(date.getUTCMonth() + 1).padStart(2, '0');
  const year = date.getUTCFullYear();
  const nasc = `${day}/${month}/${year}`;
  const sexo = ["Masculino", "Feminino"]

  
  return (
    <>
      <CustomNavbar 
      showToast={showToast} 
      setShowToast={setShowToast}
      messageToast={messageToast} 
      setMessageToast={setMessageToast}
      variantToast={variantToast} 
      setVariantToast={setVariantToast}
      />
      <Container
      className='mt-5'>
        <Card >
          <Card.Header className="text-center">Aluno {aluno[0]}</Card.Header>
          <Card.Body>
            {/* <Card.Title></Card.Title> */}
            <div
            className='d-flex flex-row justify-content-around'>
              <div 
              className='d-flex flex-column'>
                <p> <b>Cpf:</b> {aluno[1]} </p>
                <p> <b>Nome:</b> {aluno[2]} </p>
                <p> <b>Email:</b> {aluno[3]} </p>
                <p> <b>Nascimento:</b> {nasc} </p>
              </div>
              <div 
              className='d-flex flex-column'>
                <p> <b>Sexo:</b> {sexo} </p>
                <p> <b>Cep:</b> {aluno[6]} </p>
                <p> <b>Celular:</b> {aluno[7]} </p>
              </div>
            </div>
          </Card.Body>
        </Card>
        <div
        className='d-flex flex-row justify-content-around mt-3'>
        <Button
        onClick={() => setModalEditar(true)}>
          Editar Aluno
        </Button>
        <Button 
        variant='danger'
        onClick={() => setModalExcluir(true)}>
          Excluir Aluno
        </Button>
        </div>
      </Container>
      <Modal 
      show={modalEditar} 
      onHide={() => setModalEditar(false)}
      size="lg"
      centered>
        <Modal.Header closeButton>
          <Modal.Title>Editar Aluno {aluno[0]}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group className="mb-3" controlId="formBasicEmail">
              <Form.Label>Email address</Form.Label>
              <Form.Control type="email" placeholder="Enter email" />
            </Form.Group>

            <Form.Group className="mb-3" controlId="formBasicPassword">
              <Form.Label>Password</Form.Label>
              <Form.Control type="password" placeholder="Password" />
            </Form.Group>
            <Form.Group className="mb-3" controlId="formBasicCheckbox">
              <Form.Check type="checkbox" label="Check me out" />
            </Form.Group>
            
            <Button variant="primary" type="submit">
              Submit
            </Button>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setModalEditar(false)}>
            Fechar
          </Button>
          <Button variant="primary" onClick={() => setModalEditar(false)}>
            Salvar
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}

export default Aluno;
