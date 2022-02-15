curl -X POST `
  --header "Content-Type: application/json" `
  --data '{
             ""name"": ""My Webhook"",
             ""url"": ""http://example.com/my/hook/path"",
             ""secret_token"": ""sMeyqOYenB8Czi2zGOFHNg"",
             ""on_submission"": false
         }' `
  http://dtf.example.com/api/projects/1/webhooks