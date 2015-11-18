CREATE OR REPLACE FUNCTION table_id_notify() RETURNS trigger AS $$
    /* Generic function to create notifications through triggers  */
DECLARE
  data JSON;
BEGIN
  IF (TG_OP = 'DELETE') THEN
    data = row_to_json(OLD);
  ELSE
    data = row_to_json(NEW);
  END IF;
  PERFORM pg_notify(
      TG_ARGV[0], -- Listening channel
      json_build_object('table_name',TG_TABLE_NAME::VARCHAR,
                        'operation',TG_OP::VARCHAR,
                        'data',data)::text); -- json_build_object -> Available since 9.4
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;
