curl -X PUT `
  --header "Content-Type: application/json" `
  --data '{
             ""project"": 1,
             ""id"": 1,
             ""name"": ""Demo Bot"",
             ""url"": ""http://129.26.133.164:8666/references/demo"",
             ""secret_token"": ""58a61681-f3c0-4d0f-a8bf-c87193f2603d"",
             ""on_submission"": true,
             ""on_test_result"": false,
             ""on_reference_set"": false,
             ""on_test_reference"": true
         }' `
  http://dtf.example.com/api/projects/1/webhooks/1