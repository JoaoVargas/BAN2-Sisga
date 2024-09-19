import React, { useEffect } from 'react';

import CustomNavbar from '../../components/CustomNavbar';
import CardContainer from '../../components/home/CardContainer';

const Home = () => {
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
      titulo: "Salas",
      total: "10"
    },
  ]

  // useEffect(() => {
  //   fetch('http://0.0.0.0:5002/', { 
  //       method: 'GET'
  //     })
  //     .then((res) => {
  //       console.log("res", res);
  //       return res.json();
  //     })
  //     .then((data) => {
  //       console.log("data", data);
  //     });
  // }, []);

  return (
    <>
      <CustomNavbar />
      <CardContainer valores={valores}/>

    </>
  );
}

export default Home;
