CREATE TABLE magic_project_mirror
(
  id integer not null,
  name character varying,
  description character varying,
  finished boolean,
  budget float,
  duration_days integer,
  resources character varying[],
  created_at timestamp with time zone,
  insert_date timestamp with time zone,
  CONSTRAINT magic_project_mirror_pkey PRIMARY KEY (id)
);
