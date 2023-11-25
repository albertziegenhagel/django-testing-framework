curl -X PUT \
  --header "Content-Type: application/json" \
  --data '{
             "project": 1,
             "info": {
                 "Hostname": "Vasa",
                 "Branch": "feature"
             }
         }' \
  http://dtf.example.com/api/projects/1/submissions/2