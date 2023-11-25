curl -X POST `
  --header "Content-Type: application/json" `
  --data '{
             ""property_values"": {
                 ""Hostname"": ""Vasa"",
                 ""Branch"": ""feature""
             }
         }' `
  http://dtf.example.com/api/projects/1/references