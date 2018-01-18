GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA synaps to synaps;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA synaps TO synaps;
GRANT USAGE ON SCHEMA synaps TO synaps;
    
CREATE TABLE synaps.sessions
(
    id SERIAL NOT NULL,
    start_date bigint,
    duration int,
    sex character varying(1),
    age int
);