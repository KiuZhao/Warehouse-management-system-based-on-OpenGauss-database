--
-- openGauss database dump
--

SET statement_timeout = 0;
SET xmloption = content;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET session_replication_role = replica;
SET client_min_messages = warning;
SET enable_dump_trigger_definer = on;

--
-- Name: BEHAVIORCOMPAT; Type: BEHAVIORCOMPAT; Schema: -; Owner: 
--

SET behavior_compat_options = '';


--
-- Name: LENGTHSEMANTICS; Type: LENGTHSEMANTICS; Schema: -; Owner: 
--

SET nls_length_semantics = 'byte';


SET search_path = public;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: goods; Type: TABLE; Schema: public; Owner: omm; Tablespace: 
--

CREATE TABLE goods (
    goods_id integer NOT NULL,
    goods_name character varying(100) NOT NULL,
    origin character varying(100) NOT NULL,
    goods_code character varying(50) NOT NULL,
    "number" text
)
WITH (orientation=row, compression=no);


ALTER TABLE public.goods OWNER TO omm;

--
-- Name: goods_goods_id_seq; Type: SEQUENCE; Schema: public; Owner: omm
--

CREATE  SEQUENCE goods_goods_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.goods_goods_id_seq OWNER TO omm;

--
-- Name: goods_goods_id_seq; Type: LARGE SEQUENCE OWNED BY; Schema: public; Owner: omm
--

ALTER  SEQUENCE goods_goods_id_seq OWNED BY goods.goods_id;


--
-- Name: operation_logs; Type: TABLE; Schema: public; Owner: omm; Tablespace: 
--

CREATE TABLE operation_logs (
    log_id integer NOT NULL,
    operator_username character varying(50) NOT NULL,
    operation_date timestamp(0) without time zone NOT NULL,
    operation_content text NOT NULL
)
WITH (orientation=row, compression=no);


ALTER TABLE public.operation_logs OWNER TO omm;

--
-- Name: operation_logs_log_id_seq; Type: SEQUENCE; Schema: public; Owner: omm
--

CREATE  SEQUENCE operation_logs_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.operation_logs_log_id_seq OWNER TO omm;

--
-- Name: operation_logs_log_id_seq; Type: LARGE SEQUENCE OWNED BY; Schema: public; Owner: omm
--

ALTER  SEQUENCE operation_logs_log_id_seq OWNED BY operation_logs.log_id;


--
-- Name: userdetails; Type: TABLE; Schema: public; Owner: omm; Tablespace: 
--

CREATE TABLE userdetails (
    user_detail_id integer NOT NULL,
    user_id integer NOT NULL,
    user_type_id integer NOT NULL
)
WITH (orientation=row, compression=no);


ALTER TABLE public.userdetails OWNER TO omm;

--
-- Name: userdetails_user_detail_id_seq; Type: SEQUENCE; Schema: public; Owner: omm
--

CREATE  SEQUENCE userdetails_user_detail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.userdetails_user_detail_id_seq OWNER TO omm;

--
-- Name: userdetails_user_detail_id_seq; Type: LARGE SEQUENCE OWNED BY; Schema: public; Owner: omm
--

ALTER  SEQUENCE userdetails_user_detail_id_seq OWNED BY userdetails.user_detail_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: omm; Tablespace: 
--

CREATE TABLE users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    name character varying(50) NOT NULL,
    contact_info character varying(100)
)
WITH (orientation=row, compression=no);


ALTER TABLE public.users OWNER TO omm;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: omm
--

CREATE  SEQUENCE users_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_user_id_seq OWNER TO omm;

--
-- Name: users_user_id_seq; Type: LARGE SEQUENCE OWNED BY; Schema: public; Owner: omm
--

ALTER  SEQUENCE users_user_id_seq OWNED BY users.user_id;


--
-- Name: usertypes; Type: TABLE; Schema: public; Owner: omm; Tablespace: 
--

CREATE TABLE usertypes (
    user_type_id integer NOT NULL,
    user_type_name character varying(50) NOT NULL
)
WITH (orientation=row, compression=no);


ALTER TABLE public.usertypes OWNER TO omm;

--
-- Name: usertypes_user_type_id_seq; Type: SEQUENCE; Schema: public; Owner: omm
--

CREATE  SEQUENCE usertypes_user_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.usertypes_user_type_id_seq OWNER TO omm;

--
-- Name: usertypes_user_type_id_seq; Type: LARGE SEQUENCE OWNED BY; Schema: public; Owner: omm
--

ALTER  SEQUENCE usertypes_user_type_id_seq OWNED BY usertypes.user_type_id;


--
-- Name: goods_id; Type: DEFAULT; Schema: public; Owner: omm
--

ALTER TABLE goods ALTER COLUMN goods_id SET DEFAULT nextval('goods_goods_id_seq'::regclass);


--
-- Name: log_id; Type: DEFAULT; Schema: public; Owner: omm
--

ALTER TABLE operation_logs ALTER COLUMN log_id SET DEFAULT nextval('operation_logs_log_id_seq'::regclass);


--
-- Name: user_detail_id; Type: DEFAULT; Schema: public; Owner: omm
--

ALTER TABLE userdetails ALTER COLUMN user_detail_id SET DEFAULT nextval('userdetails_user_detail_id_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: omm
--

ALTER TABLE users ALTER COLUMN user_id SET DEFAULT nextval('users_user_id_seq'::regclass);


--
-- Name: user_type_id; Type: DEFAULT; Schema: public; Owner: omm
--

ALTER TABLE usertypes ALTER COLUMN user_type_id SET DEFAULT nextval('usertypes_user_type_id_seq'::regclass);


--
-- Data for Name: goods; Type: TABLE DATA; Schema: public; Owner: omm
--

COPY public.goods (goods_id, goods_name, origin, goods_code, "number") FROM stdin;
1	青岛啤酒1	广州	A99	97
2	冰箱	青岛	B2	55
3	3	3	3	3
4	4	保金	4114514	858
\.
;

--
-- Name: goods_goods_id_seq; Type: SEQUENCE SET; Schema: public; Owner: omm
--

SELECT pg_catalog.setval('goods_goods_id_seq', 1, false);


--
-- Data for Name: operation_logs; Type: TABLE DATA; Schema: public; Owner: omm
--

COPY public.operation_logs (log_id, operator_username, operation_date, operation_content) FROM stdin;
1	warehousestaff	2025-06-16 00:00:00	123
2	warehousestaff	2025-06-16 00:00:00	期末周
3	warehousestaff	2025-06-18 00:00:00	12345
\.
;

--
-- Name: operation_logs_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: omm
--

SELECT pg_catalog.setval('operation_logs_log_id_seq', 3, true);


--
-- Data for Name: userdetails; Type: TABLE DATA; Schema: public; Owner: omm
--

COPY public.userdetails (user_detail_id, user_id, user_type_id) FROM stdin;
1	1	1
4	2	2
5	3	3
\.
;

--
-- Name: userdetails_user_detail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: omm
--

SELECT pg_catalog.setval('userdetails_user_detail_id_seq', 10, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: omm
--

COPY public.users (user_id, username, password, name, contact_info) FROM stdin;
1	admin	Aa@12345	ZhangSan	123123123
2	procurementstaff	Pp@12345	LiSi	456456456
3	warehousestaff	Ww@12345	WangWui	789789789
\.
;

--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: omm
--

SELECT pg_catalog.setval('users_user_id_seq', 5, true);


--
-- Data for Name: usertypes; Type: TABLE DATA; Schema: public; Owner: omm
--

COPY public.usertypes (user_type_id, user_type_name) FROM stdin;
1	System Admin
2	Procurement Staff
3	Warehouse Staff
\.
;

--
-- Name: usertypes_user_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: omm
--

SELECT pg_catalog.setval('usertypes_user_type_id_seq', 3, true);


--
-- Name: goods_goods_code_key; Type: CONSTRAINT; Schema: public; Owner: omm; Tablespace: 
--

ALTER TABLE goods
    ADD CONSTRAINT goods_goods_code_key UNIQUE (goods_code);


--
-- Name: goods_pkey; Type: CONSTRAINT; Schema: public; Owner: omm; Tablespace: 
--

ALTER TABLE goods
    ADD CONSTRAINT goods_pkey PRIMARY KEY  (goods_id);


--
-- Name: operation_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: omm; Tablespace: 
--

ALTER TABLE operation_logs
    ADD CONSTRAINT operation_logs_pkey PRIMARY KEY  (log_id);


--
-- Name: userdetails_pkey; Type: CONSTRAINT; Schema: public; Owner: omm; Tablespace: 
--

ALTER TABLE userdetails
    ADD CONSTRAINT userdetails_pkey PRIMARY KEY  (user_detail_id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: omm; Tablespace: 
--

ALTER TABLE users
    ADD CONSTRAINT users_pkey PRIMARY KEY  (user_id);


--
-- Name: users_username_key; Type: CONSTRAINT; Schema: public; Owner: omm; Tablespace: 
--

ALTER TABLE users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: usertypes_pkey; Type: CONSTRAINT; Schema: public; Owner: omm; Tablespace: 
--

ALTER TABLE usertypes
    ADD CONSTRAINT usertypes_pkey PRIMARY KEY  (user_type_id);


--
-- Name: usertypes_user_type_name_key; Type: CONSTRAINT; Schema: public; Owner: omm; Tablespace: 
--

ALTER TABLE usertypes
    ADD CONSTRAINT usertypes_user_type_name_key UNIQUE (user_type_name);


--
-- Name: userdetails_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: omm
--

ALTER TABLE userdetails
    ADD CONSTRAINT userdetails_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE;


--
-- Name: userdetails_user_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: omm
--

ALTER TABLE userdetails
    ADD CONSTRAINT userdetails_user_type_id_fkey FOREIGN KEY (user_type_id) REFERENCES usertypes(user_type_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: omm
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM omm;
GRANT CREATE,USAGE ON SCHEMA public TO omm;
GRANT USAGE ON SCHEMA public TO PUBLIC;
GRANT CREATE,USAGE ON SCHEMA public TO dbuser;


--
-- Name: goods; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON TABLE goods FROM PUBLIC;
REVOKE ALL ON TABLE goods FROM omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE goods TO omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE goods TO dbuser;
GRANT COMMENT,ALTER,DROP,INDEX,VACUUM ON TABLE goods TO dbuser;


--
-- Name: goods_goods_id_seq; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON SEQUENCE goods_goods_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE goods_goods_id_seq FROM omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE goods_goods_id_seq TO omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE goods_goods_id_seq TO dbuser;
GRANT COMMENT,ALTER,DROP ON SEQUENCE goods_goods_id_seq TO dbuser;


--
-- Name: operation_logs; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON TABLE operation_logs FROM PUBLIC;
REVOKE ALL ON TABLE operation_logs FROM omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE operation_logs TO omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE operation_logs TO dbuser;
GRANT COMMENT,ALTER,DROP,INDEX,VACUUM ON TABLE operation_logs TO dbuser;


--
-- Name: operation_logs_log_id_seq; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON SEQUENCE operation_logs_log_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE operation_logs_log_id_seq FROM omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE operation_logs_log_id_seq TO omm;
GRANT SELECT,USAGE ON SEQUENCE operation_logs_log_id_seq TO dbuser;


--
-- Name: userdetails; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON TABLE userdetails FROM PUBLIC;
REVOKE ALL ON TABLE userdetails FROM omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE userdetails TO omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE userdetails TO dbuser;
GRANT COMMENT,ALTER,DROP,INDEX,VACUUM ON TABLE userdetails TO dbuser;


--
-- Name: userdetails_user_detail_id_seq; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON SEQUENCE userdetails_user_detail_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE userdetails_user_detail_id_seq FROM omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE userdetails_user_detail_id_seq TO omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE userdetails_user_detail_id_seq TO dbuser;
GRANT COMMENT,ALTER,DROP ON SEQUENCE userdetails_user_detail_id_seq TO dbuser;


--
-- Name: users; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON TABLE users FROM PUBLIC;
REVOKE ALL ON TABLE users FROM omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE users TO omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE users TO dbuser;
GRANT COMMENT,ALTER,DROP,INDEX,VACUUM ON TABLE users TO dbuser;


--
-- Name: users_user_id_seq; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON SEQUENCE users_user_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE users_user_id_seq FROM omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE users_user_id_seq TO omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE users_user_id_seq TO dbuser;
GRANT COMMENT,ALTER,DROP ON SEQUENCE users_user_id_seq TO dbuser;


--
-- Name: usertypes; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON TABLE usertypes FROM PUBLIC;
REVOKE ALL ON TABLE usertypes FROM omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE usertypes TO omm;
GRANT SELECT,INSERT,REFERENCES,DELETE,TRIGGER,TRUNCATE,UPDATE ON TABLE usertypes TO dbuser;
GRANT COMMENT,ALTER,DROP,INDEX,VACUUM ON TABLE usertypes TO dbuser;


--
-- Name: usertypes_user_type_id_seq; Type: ACL; Schema: public; Owner: omm
--

REVOKE ALL ON SEQUENCE usertypes_user_type_id_seq FROM PUBLIC;
REVOKE ALL ON SEQUENCE usertypes_user_type_id_seq FROM omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE usertypes_user_type_id_seq TO omm;
GRANT SELECT,USAGE,UPDATE ON SEQUENCE usertypes_user_type_id_seq TO dbuser;
GRANT COMMENT,ALTER,DROP ON SEQUENCE usertypes_user_type_id_seq TO dbuser;


--
-- openGauss database dump complete
--

