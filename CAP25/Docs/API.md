# API Docs

## Base URL
`http://localhost:8888`

Notice the webserver reject any request from remote IP is not `127.0.0.1` (IPV4) or `::1` (IPV6) for the security reason.

## Endpoints


### `POST /file/upload` - File Upload
Accepts Student/Company CSV files  
**Parameters:**
```json
{"filearg": <CSV FILE>, "file_type": "Student" | "Company"}
```

**Success:**  
`"<filename> uploaded"`

### `POST /matching` - Get Current Allocation
Returns mock matching data  

> The skill set section is probably not suitable in the current case, we probably need to change the skill-set into a dictionary instead of list; more or less like {1: 5, 2: 3, 3:4 ...}

**Response:**  
```json
{
  "students": [{"name": "abcd", "eid": 1234, "skill_set": [2,3]}...],
  "projects": [{"name": "Project A", "skill_req": [0,1]}...],
  "skills": {"0": "AI", "1": "Analogue Circuit"...}
}
```

### `POST /action/solve` - Start solver at background

Returns status of solver

**Response:**

if file is in right format, and solver started, server will return:
```json
{"result": "success", "msg": "solver started"}
```

if problem occured, the server will return:

```json
{"result": "success", "msg": 
      "existing an ongoing solver"
    | "student file does not exist, please upload that first"
    | "company file does not exist, please upload that first"
}
```

> in future version we would probably have the format checker block running, returning with the error in the format of the uploaded file. So the message section is not fixed to current three possibility
