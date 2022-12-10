#!/bin/bash

sleep 10

alembic upgrade head
echo 'Migrations executed'

exec uvicorn main:app --reload --host 0.0.0.0 --port 8000
