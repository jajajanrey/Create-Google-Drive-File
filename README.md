# CREATE A FILE IN GOOGLE DRIVE

A [Supercode](http://gosupercode.com) function that creates file in google drive

## Sample Usage

[Supercode](http://gosupercode.com) SDK will be available after the launch.

```
import json
import pprint
import supercode

response = supercode.call(
    "super-code-function",
    "your-supercode-api-key",
    folder_id="PARENT_FOLDER_ID_HERE",
    mime_type="FILE_MIMETYPE"
    domain_list=[],
    email_list=[],
    service_account_json={SERVICE_ACCOUNT_JSON}
)

    
pprint(response)
```

**Note:** Supercode has not been launched yet. This is for internal testing only.