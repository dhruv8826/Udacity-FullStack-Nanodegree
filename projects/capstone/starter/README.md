# Full Stack EmpComp Details App API Backend

## About

The project provides the complete backend to create and view company-employee records. It acts as a repository for company-employee data. Employees can manage their information including their details and the companies they work for. System Manager manages the whole system, from company records to employee records including retrival of the summary data for both employees and companies across the repository.

---------------------<heruko link>--------------------------
---------------------<how to generate auth token and related stuff>-------------------------------



## API

In order to use the API users need to be authentiated. User can have either of the 2 roles- an employee or system manager.


### endpoints for EMPLOYEE data

1. Get By Employee Id
```

GET '/employee/<employee_id>'
- Fetches the data for the employee by its id
- Request Argument: None
- Roles Required: employee or system manager
- Returns:
{
    'success': True,
    'data': {
        'employee_details': {
            'id': 1,
            'first name': 'firstname',
            'last name': 'lastname'
        },
        'companies_worked_for': [
            {
                'company_id': 1
            },
            {
                'company_id': 2
            }
        ]
    }
}

```

2. Get All Employee Details
```

GET '/employee/all'
- Fetches the list of all the employees and its details in the registry
- Request Argument: None
- Roles Required: system manager
- Returns:
{
    'success': True,
    'data': [
        {
        'employee_details': {
            'id': 1,
            'first name': 'firstname',
            'last name': 'lastname'
        },
        'companies_worked_for': [
            {
                'company_id': 1
            },
            {
                'company_id': 2
            }
        ]},
        {
        'employee_details': {
            'id': 2,
            'first name': 'firstname2',
            'last name': 'lastname2'
        },
        'companies_worked_for': [
            {
                'company_id': 2
            },
            {
                'company_id': 3
            }
        ]}
    ]
}

```

3. Post Employee Details
```

POST '/employee'
- Creates employee record in the repository
- Request Argument: json object
{
    'firstname': 'FirstName1',
    'lastname': 'LastName1',
    'works_in': {
        'company_id': 1
    }
}
- Roles Required: employee or system manager
- Returns:
{
    'success': True,
    'data': {
        'employee_details': {
            'id': 3,
            'first name': 'Firstname1',
            'last name': 'Lastname1'
        },
        'companies_worked_for': [
            {
                'company_id': 1
            }
        ]
    }
}

```

4. Patch Employee Details
```

PATCH '/employee/<employee_id>'
- Update employee record in the repository
- Request Argument: json object (all attributes not required, even a single one to be updated can be sent)
{
    'firstname': 'FirstNewName1',
    'lastname': 'LastNewName1'
}
- Roles Required: employee or system manager
- Returns:
{
    'success': True,
    'data': {
        'employee_details': {
            'id': 3,
            'first name': 'FirstNewname1',
            'last name': 'LastNewname1'
        }
    }
}

```

5. Delete Employee Details
```

DELETE '/employee/<employee_id>'
- Deletes the employee from the repository with its work details
- Request Argument: None
- Roles Required: system manager
- Returns:
{
    'success': True,
    'deleted_id': 3
}

```


### endpoints for COMPANY data

1. Get By Company Id
```

GET '/company/<company_id>'
- Fetches the data for the company by its id
- Request Argument: None
- Roles Required: system manager
- Returns:
{
    'success': True,
    'data': {
        'comapany_details': {
            'id': 1,
            'company name': 'First Company',
            'industry': 'First Industry'
        },
        'employees': [
            {
                'employee_id': 1
            },
            {
                'employee_id': 2
            }
        ]
    }
}

```

2. Get All Company Details
```

GET '/company/all'
- Fetches the list of all the companies in the registry
- Request Argument: None
- Roles Required: system manager
- Returns:
{
    'success': True,
    'data': [
        {
            'id': 1,
            'company name': 'Company 1',
            'industry': 'Industry 1'
        },
        {
            'id': 2,
            'company name': 'Company 2',
            'industry': 'Industry 2'
        }
    ]
}

```

3. Post Company Details
```

POST '/company'
- Creates company record in the repository
- Request Argument: json object
{
    'company_name': 'Company 1',
    'industry': 'Industry 1'
}
- Roles Required: system manager
- Returns:
{
    'success': True,
    'data': {
        'company': {
            'id': 1,
            'company name': 'Company 1',
            'industry': 'Industry 1'
        }
    }
}

```

4. Patch Company Details
```

PATCH '/company/<company_id>'
- Update company record in the repository
- Request Argument: json object (all attributes not required, even a single one to be updated can be sent)
{
    'company_name': 'New Company 7',
    'industry': 'New Industry 7'
}
- Roles Required: system manager
- Returns:
{
    'success': True,
    'data': {
        'company_details': {
            'id': 7,
            'company name': 'New Company 7',
            'industry': 'New Industry 7'
        }
    }
}

```

5. Delete Company Details
```

DELETE '/company/<comapny_id>'
- Deletes the company from the repository
- Request Argument: None
- Roles Required: system manager
- Returns:
{
    'success': True,
    'deleted_id': 3
}

```


### error response

```

An error response will be returned with an error code onr equest and with a json load that would contain a success flag as False, an error field with the corresponding error code and a message filed with the corresponding error message.
response:
{
      "success": False,
      "error": 404,
      "message": Not Found
}

```



## Installation

The following section contains steps to set-up and run project locally


### Installing Depedencies

The project requires Python 3.6. Using a virtual environment such as pipenv is recommended. Set up the project as follows:

```
pip install pipenv
```


### Database Setup

With postgres, create a database:

```
createdb -U <username> empCompDetails
```
'-U <username>' can be ignored if set as default


### Running Server

To run the server, first set the environment variables, then execute:

1. Set db varaibles
```
export DB_NAME="empCompDetails"
export DB_USER=""
export DB_PASSWORD=""
```
We need to pass Db user and password as blank strings if we use default configuration. In case a custom user exists, then the user name and password needs to be set in their respective varaibles.

2. Run the code
```
python app.py
```



## Testing

To test the API:

1. First create the test database
```
createdb -U <username> empCompDetails_Test
```

2. Set the environment variable
```
export TEST_DB_NAME="empCompDetails_Test"
```

3. Execute the test
```
python test_app.py
```