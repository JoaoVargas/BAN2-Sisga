import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';
import Home from './src/routes/home/Home';
import Null from './src/routes/Null/Null';
import Alunos from './src/routes/alunos/Alunos';
import Aluno from './src/routes/alunos/Aluno';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={
          <Navigate to="/home" />
        }/>
        <Route path="/home" element={< Home />}/>
        <Route path="/alunos" element={< Alunos />}/>
        <Route path="/alunos/:cod_aluno" element={< Aluno />}/>
        <Route path="*" element={<Null />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
