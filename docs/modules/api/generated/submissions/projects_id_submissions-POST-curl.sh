curl -X POST \
  --header "Content-Type: application/json" \
  --data '{
             "info": {
                 "Hostname": "Vasa",
                 "Branch": "feature"
             }
         }' \
  http://dtf.example.com/api/projects/1/submissions