import React from 'react';
import { useNavigate } from "react-router-dom";

import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
import NavDropdown from 'react-bootstrap/NavDropdown';


const CustomNavbar = () => {
  const navigate = useNavigate();
  

  return (
    <Navbar 
    expand="lg" 
    className="bg-body-tertiary">
      <Container>
        <Navbar.Brand 
        onClick={() => navigate("/home")}>
          SISGA
        </Navbar.Brand>
        <Navbar.Toggle 
        aria-controls="basic-navbar-nav" />
        <Navbar.Collapse 
        id="basic-navbar-nav">
          <Nav 
          className="me-auto">
            <Nav.Link 
            onClick={() => navigate("/aluno")}>
              Alunos
            </Nav.Link>
            <Nav.Link 
            onClick={() => navigate("/professor")}>
              Professores
            </Nav.Link>
            <Nav.Link 
            onClick={() => navigate("/coordenador")}>
              Coordenadores
            </Nav.Link>
            <Nav.Link 
            onClick={() => navigate("/coordenador")}>
              Inicializar Dados no Banco
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default CustomNavbar;
