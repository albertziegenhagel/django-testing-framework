curl -X PUT \
  --header "Content-Type: application/json" \
  --data '{
             "submission": 1,
             "name": "demo (np=1)",
             "status": "failed"
         }' \
  http://dtf.example.com/api/projects/1/tests/1