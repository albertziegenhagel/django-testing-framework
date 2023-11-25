curl -X POST `
  --header "Content-Type: application/json" `
  --data '{
             ""test_name"": ""New Test"",
             ""default_source"": 2,
             ""references"": {
                 ""runtime"": {
                     ""value"": {
                         ""data"": ""PT0.124356S"",
                         ""type"": ""duration""
                     },
                     ""source"": 1
                 },
                 ""Result1"": {
                     ""value"": {
                         ""data"": 123,
                         ""type"": ""integer""
                     }
                 }
             }
         }' `
  http://dtf.example.com/api/projects/1/references/1/tests