curl -X POST \
  --header "Content-Type: application/json" \
  --data '{
             "name": "New Measurement",
             "status": "failed",
             "value": {
                 "data": 123,
                 "type": "integer"
             },
             "reference": {
                 "data": 42,
                 "type": "integer"
             },
             "reference_source": 1
         }' \
  http://dtf.example.com/api/projects/1/tests/2/measurements