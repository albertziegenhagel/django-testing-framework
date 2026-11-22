curl -X POST \
  --header "Content-Type: application/json" \
  --data '{
             "name": "New Measurement",
             "status": "unknown",
             "value": {
                 "data": 42,
                 "type": "integer"
             },
             "reference": null
         }' \
  http://dtf.example.com/api/projects/1/tests/1/measurements