curl -X POST \
  --header "Content-Type: application/json" \
  --data '{
             "name": "New Test",
             "results": [
                 {
                     "name": "runtime",
                     "value": {
                         "data": "PT0.124356S",
                         "type": "duration"
                     },
                     "status": "failed",
                     "reference": null
                 }
             ]
         }' \
  http://dtf.example.com/api/projects/1/submissions/1/tests