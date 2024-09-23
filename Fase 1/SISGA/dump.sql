--
-- PostgreSQL database dump
--

-- Dumped from database version 12.20
-- Dumped by pg_dump version 12.20

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;



--
-- Name: alunos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alunos (
    cod_aluno integer NOT NULL,
    cpf character varying(11) NOT NULL
);


--
-- Name: alunos_codAluno_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."alunos_codAluno_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: alunos_codAluno_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."alunos_codAluno_seq" OWNED BY public.alunos.cod_aluno;


--
-- Name: coordenadores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.coordenadores (
    cod_coordenador integer NOT NULL,
    cpf character varying(11) NOT NULL,
    salario real NOT NULL,
    CONSTRAINT salario_check CHECK ((salario >= (0)::double precision))
);


--
-- Name: coordenadores_codCoordenador_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."coordenadores_codCoordenador_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: coordenadores_codCoordenador_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."coordenadores_codCoordenador_seq" OWNED BY public.coordenadores.cod_coordenador;


--
-- Name: curso_disciplinas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.curso_disciplinas (
    cod_curso_disciplina integer NOT NULL,
    cod_curso integer NOT NULL,
    cod_disciplina integer NOT NULL
);


--
-- Name: curso_disciplinas_cod_curso_disciplina_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.curso_disciplinas_cod_curso_disciplina_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: curso_disciplinas_cod_curso_disciplina_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.curso_disciplinas_cod_curso_disciplina_seq OWNED BY public.curso_disciplinas.cod_curso_disciplina;


--
-- Name: cursos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.cursos (
    cod_curso integer NOT NULL,
    nome character varying(100) NOT NULL,
    periodo character varying(1) NOT NULL,
    credito_total integer NOT NULL,
    cod_coordenador integer NOT NULL,
    CONSTRAINT credito_total_check CHECK ((credito_total >= 0))
);


--
-- Name: cursos_cod_curso_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.cursos_cod_curso_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: cursos_cod_curso_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.cursos_cod_curso_seq OWNED BY public.cursos.cod_curso;


--
-- Name: disciplinas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.disciplinas (
    cod_disciplina integer NOT NULL,
    nome character varying(50) NOT NULL,
    fase integer NOT NULL,
    creditos integer NOT NULL,
    CONSTRAINT creditos_check CHECK ((creditos >= 0)),
    CONSTRAINT fase_check CHECK ((fase > 0))
);


--
-- Name: disciplinas_cod_disciplina_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.disciplinas_cod_disciplina_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: disciplinas_cod_disciplina_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.disciplinas_cod_disciplina_seq OWNED BY public.disciplinas.cod_disciplina;


--
-- Name: historicos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.historicos (
    cod_historico integer NOT NULL,
    cod_aluno integer NOT NULL,
    cod_disciplina integer NOT NULL,
    nota_geral real NOT NULL,
    frequencia_geral real NOT NULL,
    aprovacao_final boolean NOT NULL
);


--
-- Name: historico_cod_historico_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.historico_cod_historico_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: historico_cod_historico_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.historico_cod_historico_seq OWNED BY public.historicos.cod_historico;


--
-- Name: pessoas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pessoas (
    cpf character varying(11) NOT NULL,
    nome character varying(100) NOT NULL,
    sexo integer,
    cep character varying(8),
    email character varying(50) NOT NULL,
    data_nascimento date NOT NULL,
    telefone character varying(14) NOT NULL
);


--
-- Name: professores; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.professores (
    cod_professor integer NOT NULL,
    cpf character varying(11) NOT NULL,
    salario real NOT NULL,
    formacao character varying(25),
    CONSTRAINT salario_check CHECK ((salario >= (0)::double precision))
);


--
-- Name: professores_codProfessor_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."professores_codProfessor_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: professores_codProfessor_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."professores_codProfessor_seq" OWNED BY public.professores.cod_professor;


--
-- Name: relatorios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.relatorios (
    cod_relatorio integer NOT NULL,
    cod_aluno integer NOT NULL,
    cod_turma integer NOT NULL,
    notas real[],
    faltas date[]
);


--
-- Name: relatorios_cod_relatorio_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.relatorios_cod_relatorio_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: relatorios_cod_relatorio_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.relatorios_cod_relatorio_seq OWNED BY public.relatorios.cod_relatorio;


--
-- Name: turmas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.turmas (
    cod_turma integer NOT NULL,
    sala character varying(10) NOT NULL,
    max_alunos integer NOT NULL,
    agenda json NOT NULL,
    cod_disciplina integer NOT NULL,
    cod_professor integer NOT NULL,
    CONSTRAINT max_alunos_check CHECK ((max_alunos >= 0))
);


--
-- Name: turmas_cod_turma_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.turmas_cod_turma_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: turmas_cod_turma_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.turmas_cod_turma_seq OWNED BY public.turmas.cod_turma;


--
-- Name: alunos cod_aluno; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alunos ALTER COLUMN cod_aluno SET DEFAULT nextval('public."alunos_codAluno_seq"'::regclass);


--
-- Name: coordenadores cod_coordenador; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordenadores ALTER COLUMN cod_coordenador SET DEFAULT nextval('public."coordenadores_codCoordenador_seq"'::regclass);


--
-- Name: curso_disciplinas cod_curso_disciplina; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.curso_disciplinas ALTER COLUMN cod_curso_disciplina SET DEFAULT nextval('public.curso_disciplinas_cod_curso_disciplina_seq'::regclass);


--
-- Name: cursos cod_curso; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cursos ALTER COLUMN cod_curso SET DEFAULT nextval('public.cursos_cod_curso_seq'::regclass);


--
-- Name: disciplinas cod_disciplina; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disciplinas ALTER COLUMN cod_disciplina SET DEFAULT nextval('public.disciplinas_cod_disciplina_seq'::regclass);


--
-- Name: historicos cod_historico; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historicos ALTER COLUMN cod_historico SET DEFAULT nextval('public.historico_cod_historico_seq'::regclass);


--
-- Name: professores cod_professor; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.professores ALTER COLUMN cod_professor SET DEFAULT nextval('public."professores_codProfessor_seq"'::regclass);


--
-- Name: relatorios cod_relatorio; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.relatorios ALTER COLUMN cod_relatorio SET DEFAULT nextval('public.relatorios_cod_relatorio_seq'::regclass);


--
-- Name: turmas cod_turma; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.turmas ALTER COLUMN cod_turma SET DEFAULT nextval('public.turmas_cod_turma_seq'::regclass);


--
-- Data for Name: alunos; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: coordenadores; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: curso_disciplinas; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: cursos; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: disciplinas; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: historicos; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: pessoas; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: professores; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: relatorios; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Data for Name: turmas; Type: TABLE DATA; Schema: public; Owner: -
--



--
-- Name: alunos_codAluno_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."alunos_codAluno_seq"', 1, false);


--
-- Name: coordenadores_codCoordenador_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."coordenadores_codCoordenador_seq"', 1, false);


--
-- Name: curso_disciplinas_cod_curso_disciplina_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.curso_disciplinas_cod_curso_disciplina_seq', 1, false);


--
-- Name: cursos_cod_curso_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.cursos_cod_curso_seq', 1, false);


--
-- Name: disciplinas_cod_disciplina_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.disciplinas_cod_disciplina_seq', 1, false);


--
-- Name: historico_cod_historico_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.historico_cod_historico_seq', 1, false);


--
-- Name: professores_codProfessor_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public."professores_codProfessor_seq"', 1, false);


--
-- Name: relatorios_cod_relatorio_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.relatorios_cod_relatorio_seq', 1, false);


--
-- Name: turmas_cod_turma_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.turmas_cod_turma_seq', 1, false);


--
-- Name: coordenadores codCoordenador_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordenadores
    ADD CONSTRAINT "codCoordenador_pk" PRIMARY KEY (cod_coordenador);


--
-- Name: alunos cod_aluno_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alunos
    ADD CONSTRAINT cod_aluno_pk PRIMARY KEY (cod_aluno);


--
-- Name: curso_disciplinas cod_curso_disciplina_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.curso_disciplinas
    ADD CONSTRAINT cod_curso_disciplina_pk PRIMARY KEY (cod_curso_disciplina);


--
-- Name: cursos cod_curso_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cursos
    ADD CONSTRAINT cod_curso_pk PRIMARY KEY (cod_curso);


--
-- Name: disciplinas cod_disciplina_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.disciplinas
    ADD CONSTRAINT cod_disciplina_pk PRIMARY KEY (cod_disciplina);


--
-- Name: historicos cod_historico_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historicos
    ADD CONSTRAINT cod_historico_pk PRIMARY KEY (cod_historico);


--
-- Name: professores cod_professor_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.professores
    ADD CONSTRAINT cod_professor_pk PRIMARY KEY (cod_professor);


--
-- Name: relatorios cod_relatorio_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.relatorios
    ADD CONSTRAINT cod_relatorio_pk PRIMARY KEY (cod_relatorio);


--
-- Name: turmas cod_turma_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.turmas
    ADD CONSTRAINT cod_turma_pk PRIMARY KEY (cod_turma);


--
-- Name: pessoas pessoas_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pessoas
    ADD CONSTRAINT pessoas_pk PRIMARY KEY (cpf);


--
-- Name: relatorios cod_aluno_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.relatorios
    ADD CONSTRAINT cod_aluno_fk FOREIGN KEY (cod_aluno) REFERENCES public.alunos(cod_aluno) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: historicos cod_aluno_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historicos
    ADD CONSTRAINT cod_aluno_fk FOREIGN KEY (cod_aluno) REFERENCES public.alunos(cod_aluno) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: curso_disciplinas cod_curso_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.curso_disciplinas
    ADD CONSTRAINT cod_curso_fk FOREIGN KEY (cod_curso) REFERENCES public.cursos(cod_curso) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: curso_disciplinas cod_disciplina_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.curso_disciplinas
    ADD CONSTRAINT cod_disciplina_fk FOREIGN KEY (cod_disciplina) REFERENCES public.disciplinas(cod_disciplina) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- Name: turmas cod_disciplina_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.turmas
    ADD CONSTRAINT cod_disciplina_fk FOREIGN KEY (cod_disciplina) REFERENCES public.disciplinas(cod_disciplina) ON UPDATE CASCADE;


--
-- Name: historico cod_disciplina_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.historicos
    ADD CONSTRAINT cod_disciplina_fk FOREIGN KEY (cod_disciplina) REFERENCES public.disciplinas(cod_disciplina) ON UPDATE CASCADE NOT VALID;


--
-- Name: turmas cod_professor_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.turmas
    ADD CONSTRAINT cod_professor_fk FOREIGN KEY (cod_professor) REFERENCES public.professores(cod_professor) ON UPDATE CASCADE NOT VALID;


--
-- Name: relatorios cod_turma_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.relatorios
    ADD CONSTRAINT cod_turma_fk FOREIGN KEY (cod_turma) REFERENCES public.turmas(cod_turma) ON UPDATE CASCADE NOT VALID;


--
-- Name: coordenadores cpf_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.coordenadores
    ADD CONSTRAINT cpf_fk FOREIGN KEY (cpf) REFERENCES public.pessoas(cpf) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: professores cpf_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.professores
    ADD CONSTRAINT cpf_fk FOREIGN KEY (cpf) REFERENCES public.pessoas(cpf) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: alunos cpf_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alunos
    ADD CONSTRAINT cpf_fk FOREIGN KEY (cpf) REFERENCES public.pessoas(cpf) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: cursos cursos_cod_coordenador_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.cursos
    ADD CONSTRAINT cursos_cod_coordenador_fkey FOREIGN KEY (cod_coordenador) REFERENCES public.coordenadores(cod_coordenador) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

