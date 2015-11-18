/**** SCHEMA *****/

\i ./schemas/create_core.sql

/**** TABLES *****/

\i ./model/magic_project.sql
\i ./model/magic_project_mirror.sql

/**** FUNCTIONS *****/

\i ./functions/table_id_notify.sql

/**** TRIGGERS *****/

\i ./triggers/magic_project_notify.sql
