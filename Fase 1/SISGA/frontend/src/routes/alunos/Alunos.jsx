import React, { useEffect, useState } from 'react';
import CustomNavbar from '../../components/CustomNavbar';
import CustomAlunosTable from '../../components/alunos/CustomAlunosTable';

function useForceUpdate(){
  const [value, setValue] = useState(0);
  return () => setValue(value => value + 1);
}

const Alunos = () => {
  const [showToast, setShowToast] = useState(false);
  const [messageToast, setMessageToast] = useState('');
  const [variantToast, setVariantToast] = useState('');
  const forceUpdate = useForceUpdate();

  const [alunos, setAlunos] = useState([]);


  useEffect(() => {
    fetch('http://0.0.0.0:5002/alunos', { 
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })
    .then((res) => res.json())
    .then((dataAlunos) => {
      let tempAlunos = dataAlunos;
      dataAlunos.map((aluno, id) => {
        fetch(`http://0.0.0.0:5002/pessoas/${aluno[1]}`, { 
          method: 'GET',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        })
        .then((res) => res.json())
        .then((dataPessoa) => {
          tempAlunos[id] = tempAlunos[id].concat(dataPessoa[1], dataPessoa[2], dataPessoa[3], dataPessoa[4], dataPessoa[5], dataPessoa[6])
        })
      })
      setAlunos(tempAlunos)
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
