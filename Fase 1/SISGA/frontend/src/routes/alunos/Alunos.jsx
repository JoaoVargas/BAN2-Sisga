import React, { useEffect, useState } from 'react';
import CustomNavbar from '../../components/CustomNavbar';
import CustomAlunosTable from '../../components/alunos/CustomAlunosTable';

const Alunos = () => {
  const [showToast, setShowToast] = useState(false);
  const [messageToast, setMessageToast] = useState('');
  const [variantToast, setVariantToast] = useState('');

  const [alunos, setAlunos] = useState([]);

  useEffect(() => {
    fetch('http://0.0.0.0:5002/alunospessoas', { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then((res) => res.json())
    .then((dataAlunos) => {
      console.log(dataAlunos);
      setAlunos(dataAlunos);
    })
  }, []);

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
      <CustomAlunosTable alunos={alunos}/>
      
    </>
  );
}

export default Alunos;
