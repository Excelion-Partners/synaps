# #!/usr/bin/env bash

# Adding persistent data folder
if [ ! -d "$PGDATA" ]; then
    echo "Postgres data directory does not exist.  Creating..."
    mkdir -p $PGDATA
fi

# Adding persistent postgres log folder
if [ ! -d "$PGLOG" ]; then
    echo "Postgres logging directory does not exist.  Creating..."
    mkdir -p $PGLOG
fi

# Give postgres user ownership of persistent directories
echo "Setting postgres user as owner of persistent directories..."
chown -R postgres $PGHOME

# Check if database is already initialized in persistent folder
EXISTED=0
if [ ! -f "$PGDATA/postgresql.conf" ]; then
    useradd synaps

    # Initialize database
    echo "Initializing postgress database..."
    su postgres -c "${PGCTL} init -D ${PGDATA}"
    echo "Finished initializing the database."

    EXISTED=1
fi

# Start the postgres database using the persistent data directory
echo "Starting the postgres database..."
echo "${PGCTL} start -D ${PGDATA}"
exec su postgres -c "${PGCTL} start -D ${PGDATA}" >$PGLOG/postgresql.log 2>&1 &
echo "Postgres database started."

if [ "$EXISTED" -eq "1" ]; then
    sleep 10
    echo "Creating superuser: '${PGUSER}'..."
    sudo -u postgres /usr/lib/postgresql/9.6/bin/psql -d postgres -c "ALTER USER postgres PASSWORD 'postgres'"
    sudo -u postgres /usr/lib/postgresql/9.6/bin/psql -d postgres -c "CREATE USER $PGUSER WITH SUPERUSER PASSWORD '$PGPASS'"
    echo "Finished creating superuser: '${PGUSER}'."

    sudo -u postgres /usr/lib/postgresql/9.6/bin/psql -d postgres -c "ALTER USER ${PGUSER} with encrypted password '${PGPASS}';"
    sudo -u postgres /usr/lib/postgresql/9.6/bin/psql -d postgres -c "CREATE DATABASE synaps WITH OWNER = ${PGUSER} CONNECTION LIMIT = -1;"
    sudo -u synaps /usr/lib/postgresql/9.6/bin/psql -U postgres -d synaps -a -f /usr/postgres/init.sql
    sudo -u synaps /usr/lib/postgresql/9.6/bin/psql -U postgres -d synaps -a -f /usr/postgres/db_test_script.sql

    echo "Database initialized"
fi
