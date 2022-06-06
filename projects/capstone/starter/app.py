import imp
import os
from flask_security import auth_required

from sqlalchemy import and_
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from auth import AuthError, requires_auth
from flask_moment import Moment

from models import setup_db, Employee, Company, Works

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  moment = Moment(app)
  setup_db(app)
  CORS(app)
  Swagger(app)

  '''
  __ ROUTES __
  '''

  '''
  Employee
  '''
  # Create employee records
  @app.route('/employee', methods=['POST'])
  @requires_auth('post:employee')
  def post_employee(jwt):
    data = request.get_json()
    if ('firstname' not in data and 'lastname' not in data and 'works_in' not in data):
      abort(422)
    try:
      # first verify that the company employee works in is in the database
      company_id = data.get('works_in')['company_id']
      try:
        company = Company.query.get(company_id)
      except:
        abort(404)
      # check if employee details already exist in db, if not then create
      try:
        existing_employee = Employee.query.filter_by(and_(firstname=data.get('firstname'), lastname=data.get('lastname')))
        employee_id_info = existing_employee.id
      except:
        employee = Employee(firstname=data.get('firstname'), lastname=data.get('lastname'))
        employee.insert()
        employee_id_info = employee.id
      # check if woring detail exists
      try:
        existing_work_info = Works.query.filter_by(and_(employee_id=employee_id_info, company_id=company.id))
      except:
        works = Works(employee_id=employee_id_info, company_id=company.id)
        works.insert()
      
      # extract info
      employee_details = Employee.query.get(employee_id_info)
      try:
        working_details = Works.query.filter(employee_id=employee_id_info)
      except:
        working_details = []
      return jsonify({
        'success': True,
        'data': {
          'employee_details': employee_details.json_view(),
          'companies_worked_for': [w.company_json_view() for w in working_details]
        }
      }) 
    except:
      abort(422)

  # Get all employees
  @app.route('/employee/all')
  @requires_auth('get:employee-all')
  def get_all_employee(jwt):
    try:
      try:
        employees = Employee.query.all()
      except:
        abort(404)
      result_list = []
      for employee in employees:
        try:
          work_details = Works.query.filter(employee_id=employee.id).all()
        except:
          work_details = []
        result_list.append({
          'employee_details': employee.json_view(),
          'companies_worked_for': [w.company_json_view() for w in work_details]
        })
      return jsonify({
        'success': True,
        'data': result_list
      })
    except:
      abort(422)

  # Get employee by id
  @app.route('/employee/<int:id>')
  @requires_auth('get:employee')
  def get_employee(jwt, id):
    try:
      try:
        employee = Employee.query.get(id)
      except:
        abort(404)
      try:
        work_details = Works.query.filter(employee_id=employee.id).all()
      except:
        work_details = []
      return jsonify({
        'success': True,
        'data': {
          'employee_details': employee.json_view(),
          'companies_worked_for': [w.company_json_view() for w in work_details]
        }
      })
    except:
      abort(422)

  # Patch employee details
  @app.route('/employee/<int:id>', methods=['PATCH'])
  @requires_auth('patch:employee')
  def update_employee(jwt, id):
    if not id:
      abort(404)

    try:
      employee = Employee.query.get(id)
    except:
      abort(404)

    try:
      data = request.get_json()
      employee.firstname = employee.firstname if not data.get('firstname') else data.get('firstname')
      employee.lastname = employee.lastname if not data.get('lastname') else data.get('lastname')
      employee.update()
      return jsonify({
        'success': True,
        'data': {
          'employee_details': employee.json_view()
        }
      })
    except:
      abort(422)

  # Delete employee by id
  @app.route('/employee/<int:id>', methods=['DELETE'])
  @requires_auth('delete:employee')
  def delete_employee(jwt, id):
    if not id:
      abort(404)
    try:
      employee = Employee.query.get(id)
    except:
      abort(404)
    try:
      # First check if there is record for this employee in work table, if so then that needs to be deleted first
      try:
        works = Works.query.filter_by(employee_id=id).all()
      except:
        works=[]
      for work in works:
        work.delete()
      employee.delete()
      return jsonify({
        'success': True,
        'deleted_id': id
      })
    except:
      abort(422)
  

  '''
  Company
  '''
  # Create company
  @app.route('/company', methods=['POST'])
  @requires_auth('post:company')
  def post_company(jwt):
    data = request.get_json()
    if ('company_name' not in data and 'industry' not in data):
      abort(422)
    try:
      # Check if compnay exists already
      try:
        company_exists = Company.query.filter(and_(company_name=data.get('company_name'), industry=data.get('industry')))
        company = company_exists
      except:
        new_company = Company(company_name=data.get('company_name'), industry=data.get('industry'))
        new_company.insert()
        company = new_company
      return jsonify({
        'success': True,
        'data': {
          'company': company.json_view()
        }
      })
    except:
      abort(422)

  # Get all companies list
  @app.route('/company/all')
  @requires_auth('get:company-all')
  def get_all_companies(jwt):
    try:
      try:
        companies = Company.query.all()
      except:
        abort(404)
      return jsonify({
        'success': True,
        'data': [c.json_view() for c in companies]
      })
    except:
      abort(422)

  # Get company details by id
  @app.route('/company/<int:id>')
  @requires_auth('get:company')
  def get_company(jwt, id):
    try:
      try:
        company = Company.query.get(id)
      except:
        abort(404)
      try:
        employees_in_company = Works.query.filter(company_id=company.id).all()
      except:
        employees_in_company = []
      return jsonify({
        'success': True,
        'data': {
          'comapany_details': company.json_view(),
          'employees': [e.employee_json_view() for e in employees_in_company]
        }
      })
    except:
      abort(422)

  # Patch company details
  @app.route('/company/<int:id>', methods=['PATCH'])
  @requires_auth('patch:company')
  def update_company(jwt, id):
    if not id:
      abort(404)

    try:
      company = Company.query.get(id)
    except:
      abort(404)

    try:
      data = request.get_json()
      company.company_name = company.company_name if not data.get('company_name') else data.get('company_name')
      company.industry = company.industry if not data.get('industry') else data.get('industry')
      company.update()
      return jsonify({
        'success': True,
        'data': {
          'company_details': company.json_view()
        }
      })
    except:
      abort(422)

  # Delete company by id 
  @app.route('/company/<int:id>', methods=['DELETE'])
  @requires_auth('delete:company')
  def delete_company(jwt, id):
    if not id:
      abort(404)
    try:
      company = Company.query.get(id)
    except:
      abort(404)
    try:
      company.delete()
      return jsonify({
        'success': True,
        'deleted_id': id
      })
    except:
      abort(422)


  '''
  __ ERROR HANDLING __
  '''
  # handle 404
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "not found"
    }), 404

  # handle 422
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "not able to process the request"
    }), 422
    
  # handle auth error
  @app.errorhandler(AuthError)
  def handle_auth_error(error):
    return jsonify({
      "success": False,
      "error": error.status_code,
      "message": error.error
    }), error.status_code

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)