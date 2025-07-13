#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Check if both arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <database_name> <sql_file_path>"
    exit 1
fi

DB_NAME="$1"
SQL_FILE="$2"

# Check if SQL file exists
if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL file '$SQL_FILE' not found."
    exit 1
fi

# Drop all connections to the database
psql -U tourdefrance -d postgres -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '$DB_NAME' AND pid <> pg_backend_pid();"

# Drop the database
psql -U tourdefrance -d postgres -c "DROP DATABASE IF EXISTS \"$DB_NAME\";"

# Recreate the database
psql -U tourdefrance -d postgres -c "CREATE DATABASE \"$DB_NAME\";"

# Import the SQL file
psql -U tourdefrance -d "$DB_NAME" -f "$SQL_FILE"

echo "Database '$DB_NAME' has been successfully recreated and data imported."