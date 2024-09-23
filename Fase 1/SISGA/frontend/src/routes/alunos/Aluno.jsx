import React from 'react';
import { useParams } from 'react-router-dom';

const Aluno = () => {
  let { cod_aluno } = useParams();

  
  return (
    <>
      {cod_aluno}
    </>
  );
}

export default Aluno;
