import React, { useEffect, useState } from 'react';

import CustomNavbar from '../../components/CustomNavbar';
import CardContainer from '../../components/home/CardContainer';

const Home = () => {
  const [showToast, setShowToast] = useState(false);
  const [messageToast, setMessageToast] = useState('');
  const [variantToast, setVariantToast] = useState('');

  const [numPessoas, setNumPessoas] = useState(0);
  const [numCoordenadores, setNumCoordenadores] = useState(0);
  const [numProfessores, setNumProfessores] = useState(0);
  const [numAlunos, setNumAlunos] = useState(0);
  const [numCursos, setNumCursos] = useState(0);
  const [numDisciplinas, setNumDisciplinas] = useState(0);
  const [numTurmas, setNumTurmas] = useState(0);

  useEffect(() => {
    fetch('http://0.0.0.0:5002/pessoas', { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (!data) {
        setMessageToast("Erro: Get pessoas")
        setVariantToast('danger')
        setShowToast(true)
        return
      }
      setNumPessoas(data.length);
    });
    fetch('http://0.0.0.0:5002/coordenadores', { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (!data) {
        setMessageToast("Erro: Get coordenadores")
        setVariantToast('danger')
        setShowToast(true)
        return
      }
      setNumCoordenadores(data.length);
    });
    fetch('http://0.0.0.0:5002/professores', { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (!data) {
        setMessageToast("Erro: Get professores")
        setVariantToast('danger')
        setShowToast(true)
        return
      }
      setNumProfessores(data.length);
    });
    fetch('http://0.0.0.0:5002/alunos', { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (!data) {
        setMessageToast("Erro: Get alunos")
        setVariantToast('danger')
        setShowToast(true)
        return
      }
      setNumAlunos(data.length);
    });
    fetch('http://0.0.0.0:5002/alunos', { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then((res) => {
      return res.json();
    })
    .then((data) => {
      if (!data) {
        setMessageToast("Erro: Get alunos")
        setVariantToast('danger')
        setShowToast(true)
        return
      }
      setNumAlunos(data.length);
    });


    
  }, []);


  const valores = [
    {
      titulo: "Pessoas",
      total: "35"
    },
    {
      titulo: "Coordenadores",
      total: "5"
    },
    {
      titulo: "Professores",
      total: "10"
    },
    {
      titulo: "Alunos",
      total: "20"
    },
    {
      titulo: "Cursos",
      total: "5"
    },
    {
      titulo: "Disciplinas",
      total: "10"
    },
    {
      titulo: "Turmas",
      total: "10"
    },
  ]
  
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
      <CardContainer 
      valores={valores}/>

    </>
  );
}

export default Home;
