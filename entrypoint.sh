#!/bin/bash
echo "AAAAAAAA"
flask db init || true 
echo "BBBBBBBB"
flask db migrate -m "Initial migration" || true
echo "CCCCCCCC"
flask db upgrade
echo "DDDDDDDD"
exec flask run --host=0.0.0.0
