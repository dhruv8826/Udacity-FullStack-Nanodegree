import unittest
import os
import json
from wsgiref import headers

from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *

EMPLOYEE_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktXYWJ5VkF0LXctSlRFSHRQcUxILSJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYnNib2kxdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI3NjVhZGE0MDI4ZTQwMDZmZmI0ZWQ0IiwiYXVkIjoiZW1wQ29tcCIsImlhdCI6MTY1NDUyMjYwMiwiZXhwIjoxNjU0NTI5ODAyLCJhenAiOiJ6S2s1N25KV2dWb0E2Q3JSZFhOa3Y2N1JLbHNKd0MwVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmVtcGxveWVlIiwicGF0Y2g6ZW1wbG95ZWUiLCJwb3N0OmVtcGxveWVlIl19.K9xwNMqeVTX1_zU9QBrZJIQlWgJwW1a0Mf-pCrJBtgVGSvDUQFE5PAdotRXDjLhIr8DfbdtSgscgFiOMy2bjfYn-hQf2-rhs2dGvaWH3-8Lolb24qPjp36cT3TQakgLPTYXm-S7LuWKBhPhMJ-g7NLEfe_Iy6-0K6ZwrtTR9-R6oBNlUip4L9jddAzydHv2xKlBaKl6E3GI9UH6vvkzJ5qan0rrVKBuKjZVmPhITSAMrBzCj8hYnaYrhEemCqm8EjHW1oFO5QrIct2WuZcAnVopHB29o0HU4CMkGR8nXiUukx_fd-3WyFc1KoZ5r3TlAraCIY55nq9hIyHnI4v3h5Q'
ADMIN_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktXYWJ5VkF0LXctSlRFSHRQcUxILSJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYnNib2kxdS51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjI3NjVhYmJjZmM0ODEwMDY3YzI3NjVhIiwiYXVkIjoiZW1wQ29tcCIsImlhdCI6MTY1NDUyMjgyNCwiZXhwIjoxNjU0NTMwMDI0LCJhenAiOiJ6S2s1N25KV2dWb0E2Q3JSZFhOa3Y2N1JLbHNKd0MwVCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmNvbXBhbnkiLCJkZWxldGU6ZW1wbG95ZWUiLCJnZXQ6Y29tcGFueSIsImdldDpjb21wYW55LWFsbCIsImdldDplbXBsb3llZSIsImdldDplbXBsb3llZS1hbGwiLCJwYXRjaDpjb21wYW55IiwicGF0Y2g6ZW1wbG95ZWUiLCJwb3N0OmNvbXBhbnkiLCJwb3N0OmVtcGxveWVlIl19.AwHVt5FRjiDD6exrSUJGugv0q79ha02bGwoQWsWc537HcoCluNzxRwYqZ6DZP62cLSpBwh9L11ci0FBHBwTWISF1a8P78X152xbuPDSVm_oJXC1FmmkOjme613v7sw2hWKMcUdhp8wvhAUCJiDBqOcoeSn9Tmd8QnIBBLQTe4s2Bhk4DR0W4ID86ND9q61xWdz35F5-wWLjpY5nOsnLF29HqGgWUg7Iz1JtO3QEhQ3g0F0w44_zvLZQ0HHbO4PWIqM8tFep-fNmdJIBw5cNTq5RFIaBU6GmUj2BhX1HlkRpJT9SMXZbCc2JfZOYwibCWwUWhnCVi0WNQX_mVj7tUjA'

class EmpCompTestCase(unittest.TestCase):
    '''setup'''
    def setUp(self):
        '''Define Test variables and initialize app'''
        self.app = create_app()
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}
        self.database_name = os.environ['TEST_DB_NAME']
        self.user_name = os.environ['DB_USER']
        self.user_password = os.environ['DB_PASSWORD']
        if ((self.user_name is '' and self.user_password is '') or (self.user_name is None and self.user_password is None)):
            self.database_path = "postgresql:///{}".format(self.database_name)
        else:
            self.database_path = "postgresql://{}:{}@{}/{}".format(self.user_name, self.user_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        #bind app with current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

            self.db.drop_all()
            self.db.create_all()

    def tearDown(self):
        '''Executed after each test'''
        pass

    '''
    Test for Company
    '''
    def test_a_add_company(self):
        new_company = {
            'company_name': 'Test Company 1',
            'industry': 'Test Industry 1'
        }
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        res = self.client().post('/company', json=new_company, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_b_add_company_fails_without_token(self):
        new_company = {
            'company_name': 'Test Company 1',
            'industry': 'Test Industry 1'
        }

        res = self.client().post('/company', json=new_company)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401) # Headermissing error

    def test_c_add_company_fails_without_permission(self):
        new_company = {
            'company_name': 'Test Company 4',
            'industry': 'Test Industry 4'
        }
        self.headers.update({'Authorization': 'Bearer ' + EMPLOYEE_TOKEN})

        res = self.client().post('/company', json=new_company, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_d_get_company_by_id(self):
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        res = self.client().get('/company/7', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_e_get_all_companies(self):
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        res = self.client().get('/company/all', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_f_patch_company_by_id(self):
        new_company = {
            'company_name': 'Test New Company 7',
            'industry': 'Test New Industry 7'
        }
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        res = self.client().patch('/company/7', json=new_company, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_g_delete_company_by_id(self):
        # First create a company that can be deleted later
        new_company = {
            'company_name': 'Test Company to delete1',
            'industry': 'Test Industry to delete 1'
        }
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        post_res = self.client().post('/company', json=new_company, headers=self.headers)
        post_data = json.loads(post_res.data)

        self.assertEqual(post_res.status_code, 200)

        # Delete the company created
        company_id = post_data.get('data').get('company').get('id')
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        delete_res = self.client().delete('/company/' + str(company_id), headers=self.headers)
        delete_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 200)


    '''
    Test for Employee
    '''
    def test_h_add_employee(self):
        new_employee = {
            'firstname': 'TestFirstName3',
            'lastname': 'TestLastName3',
            'works_in': {
                'company_id': 7
            }
        }
        self.headers.update({'Authorization': 'Bearer ' + EMPLOYEE_TOKEN})

        res = self.client().post('/employee', json=new_employee, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_i_add_employee_by_admin(self):
        new_employee = {
            'firstname': 'TestFirstName8',
            'lastname': 'TestLastName8',
            'works_in': {
                'company_id': 7
            }
        }
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        res = self.client().post('/employee', json=new_employee, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_j_get_employee_by_id(self):
        self.headers.update({'Authorization': 'Bearer ' + EMPLOYEE_TOKEN})

        res = self.client().get('/employee/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_k_get_employee_by_id_by_admin(self):
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        res = self.client().get('/employee/1', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_l_get_all_employee(self):
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        res = self.client().get('/employee/all', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_m_should_fail_while_get_all_employee_by_employee_role(self):
        self.headers.update({'Authorization': 'Bearer ' + EMPLOYEE_TOKEN})

        res = self.client().get('/employee/all', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)

    def test_n_patch_company_by_id(self):
        new_company = {
            'firstname': 'TestFirstNewName1',
            'lastname': 'TestLastNewName1'
        }
        self.headers.update({'Authorization': 'Bearer ' + EMPLOYEE_TOKEN})

        res = self.client().patch('/employee/1', json=new_company, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_o_delete_employee_by_id(self):
        # First create employee that can be deleted later
        new_employee = {
            'firstname': 'TestFirstName3 to be deleted',
            'lastname': 'TestLastName3 to be deleted',
            'works_in': {
                'company_id': 4
            }
        }
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        post_res = self.client().post('/employee', json=new_employee, headers=self.headers)
        post_data = json.loads(post_res.data)

        self.assertEqual(post_res.status_code, 200)

        # Delete the created employee
        employee_id = post_data.get('data').get('employee_details').get('id')
        self.headers.update({'Authorization': 'Bearer ' + ADMIN_TOKEN})

        delete_res = self.client().delete('/employee/' + str(employee_id), headers=self.headers)
        delete_data = json.loads(delete_res.data)

        self.assertEqual(delete_res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()