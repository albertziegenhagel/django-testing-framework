curl -X PUT \
  --header "Content-Type: application/json" \
  --data '{
             "project": 1,
             "property_values": {
                 "Hostname": "Vasa",
                 "Branch": "main"
             }
         }' \
  http://dtf.example.com/api/projects/1/references/1