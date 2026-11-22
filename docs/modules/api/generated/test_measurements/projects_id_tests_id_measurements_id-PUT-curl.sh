curl -X PUT \
  --header "Content-Type: application/json" \
  --data '{
             "name": "runtime",
             "test_result": 1,
             "value": {
                 "data": "PT0.124356S",
                 "type": "duration"
             },
             "status": "unknown",
             "reference": null,
             "reference_source": null
         }' \
  http://dtf.example.com/api/projects/1/tests/1/measurements/1