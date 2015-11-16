/**** SCHEMA *****/

\i ./schemas/create_core.sql

/**** TABLAS *****/

\i ./model/magic_project.sql
\i ./model/magic_project_mirror.sql

/**** FUNCIONES *****/

\i ./functions/table_id_notify.sql

/**** TRIGGERS *****/

\i ./triggers/magic_project_notify.sql
