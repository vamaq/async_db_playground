CREATE SCHEMA core; -- Creates the new schema

--------------------------------------
--  Set new Schema as default on new connection.
DO
$do$
DECLARE
  search_path VARCHAR;
  current_database VARCHAR := current_database();
BEGIN
  SELECT array_to_string(ARRAY(
        SELECT DISTINCT trim(unnest(string_to_array(current_setting('search_path')||',core', ',')))
  ),',') INTO search_path;
  EXECUTE 'ALTER DATABASE '||current_database||' SET search_path TO '||search_path;
END $do$;

--------------------------------------
-- Set the new schema as default for this connection.
SET SCHEMA 'core';