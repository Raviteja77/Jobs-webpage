import json
from flask import jsonify, request
from app.models import Application, Job, User
from . import main
from app import db
from flask_restful import Resource, reqparse

class JobApplication(Resource):
    def get(self, id):
        applications = Application.query.filter(Application.user_id == id).all()
        serialized_applications = []
        for application in applications:
            serialized_application = {
                'job_id': application.job_id
            }
            serialized_applications.append(serialized_application)
        return json.dumps(serialized_applications, default=str), 200
    
    def delete(self, id):
        application = Application.query.filter(Application.job_id == id).first()
        if not application:
            return {'message': 'Job application not found', 'status': 'error'}, 404
        db.session.delete(application)
        db.session.commit()
        return {'message': 'Job application withdrawn successfully!', 'status': 'success'}, 200


class SingleJob(Resource):
    applicant_job_parser = reqparse.RequestParser()
    applicant_job_parser.add_argument('id', type=int)
    applicant_job_parser.add_argument('closed', type=bool)
    def get(self, id):
        job = Job.query.get(id)
        serialized_job = {
                    'id': job.id,
                    'job_title': job.job_title,
                    'job_description': job.job_description,
                    'company': job.company,
                    'salary_range': job.salary_range,
                    'job_category': job.job_category,
                    'email': job.email,
                    'posted_date': job.posted_date
                }
        return json.dumps(serialized_job, default=str), 200
    
    def put(self, id):
        job = Job.query.get(id)
        data = SingleJob.applicant_job_parser.parse_args()
        if data['closed']:
            job.closed = data['closed']
        db.session.add(job)
        db.session.commit()
        if data['closed']:
            return {'message': 'Job closed successfully!', 'status': 'success'}, 200
        return {'message': 'Job updated successfully!', 'status': 'success'}, 200
    
    def post(self, id):
        job = Job.query.get(id)
        data = SingleJob.applicant_job_parser.parse_args()
        user = User.query.get(data)
        application = Application(user=user, job=job)
        db.session.add(application)
        db.session.commit()
        return {'message': 'User successfully applied for the job', 'status': 'success'}, 200

class JobPosting(Resource):
    create_job_parser = reqparse.RequestParser()
    create_job_parser.add_argument('job_title', type=str, required=True, help='Job title is required')
    create_job_parser.add_argument('salary_range', type=str, required=True, help='Salary range is mandatory')
    create_job_parser.add_argument('job_category', type=str, required=True, help='Job category is required')
    create_job_parser.add_argument('company', type=str, required=True, help='Company name is required')
    create_job_parser.add_argument('job_description', type=str, required=True, help='Job description is required')
    create_job_parser.add_argument('email', type=str, required=True, help='Email is required')
    create_job_parser.add_argument('closed', type=bool, required=True, help='Job is not closed by default')
    def get(self):
        try:
            jobs = Job.query.filter(Job.closed == False).all()
            # Serialize each job object and add it to a list
            serialized_jobs = []
            for job in jobs:
                serialized_job = {
                    'id': job.id,
                    'job_title': job.job_title,
                    'job_description': job.job_description,
                    'company': job.company,
                    'salary_range': job.salary_range,
                    'job_category': job.job_category,
                    'email': job.email,
                    'posted_date': job.posted_date
                }
                serialized_jobs.append(serialized_job)
            return json.dumps(serialized_jobs, default=str), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 404
        
    def post(self):
        data = JobPosting.create_job_parser.parse_args()
        new_job = Job(job_title = data['job_title'], salary_range = data['salary_range'], company = data['company'], job_category = data['job_category'], job_description = data['job_description'], email = data['email'], closed = data['closed'])
        db.session.add(new_job)
        db.session.commit()
        return {'message': 'Posted new job successfully!', 'status': 'success'}, 200

    

# @main.route("/api/create-job", methods=["POST", "GET"])
# def create_job():
#     if request.method == 'POST':
#         job_title = request.form.get("job_title")
#         salary_range = request.form.get("salary_range")
#         company = request.form.get("company")
#         job_category = request.form.get("job_category")
#         job_description = request.form.get("job_description")
#         email = ''
#         closed = False
#         new_job = Job(job_title = job_title, salary_range = salary_range, company = company, job_category = job_category, job_description = job_description, email = email, closed = closed)
#         db.session.add(new_job)
#         db.session.commit()


# @main.route("/job-detail/<int:id>")
# def show_job(id):
#     job = Job.query.get(id)

# @main.route("/close-job/<int:id>")
# def close_job(id):
#     job = Job.query.get(id)
#     job.closed = True
#     db.session.add(job)
#     db.session.commit()

# @main.route("/applied-jobs")
# def applied_jobs():
#     user_id = ''
#     applications = Application.query.filter_by(user_id=user_id).all()
#     jobs = [application.job for application in applications]

# @main.route("/applicant-applied-jobs/<int:id>")
# def applicant_jobs(id):
#     job = Job.query.get(id)
#     user = ''
#     application = Application(user=user, job=job)
#     db.session.add(application)
#     db.session.commit()

# @main.route("/applicants-list")
# def applicants():
#     applications = Application.query.all()