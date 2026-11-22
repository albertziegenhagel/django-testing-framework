curl -X PUT `
  --header "Content-Type: application/json" `
  --data '{
             ""reference_set"": 1,
             ""test_name"": ""demo (np=1)"",
             ""measurements"": [
                 {
                     ""name"": ""runtime"",
                     ""value"": {
                         ""data"": ""PT0.124356S"",
                         ""type"": ""duration""
                     },
                     ""source"": 1
                 },
                 {
                     ""name"": ""residual[0]"",
                     ""value"": {
                         ""data"": 2.345,
                         ""type"": ""float""
                     },
                     ""source"": 1
                 },
                 {
                     ""name"": ""integer[0]"",
                     ""value"": {
                         ""data"": 98,
                         ""type"": ""integer""
                     },
                     ""source"": 1
                 },
                 {
                     ""name"": ""algorithm-time[0]"",
                     ""value"": {
                         ""data"": ""PT0.345000S"",
                         ""type"": ""duration""
                     },
                     ""source"": 1
                 },
                 {
                     ""name"": ""argument[0]"",
                     ""value"": {
                         ""data"": ""process argument 1"",
                         ""type"": ""string""
                     },
                     ""source"": 1
                 }
             ]
         }' `
  http://dtf.example.com/api/projects/1/references/1/tests/1