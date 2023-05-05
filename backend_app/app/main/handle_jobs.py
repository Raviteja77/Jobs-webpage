import json
from flask import jsonify
from app.models import Application, Job, User
from . import main
from app import db
from flask_restful import Resource, reqparse

class Applicants(Resource):
    # Define a request parser to parse the email input parameter
    applicant_parser = reqparse.RequestParser()
    applicant_parser.add_argument('email', type=str)

    def get(self):
        # Parse the email input parameter from the request
        data = Applicants.applicant_parser.parse_args()
        # Retrieve all jobs that have the given email as the contact email
        jobs = Job.query.filter_by(email=data['email']).all()
        job_applications = []
        # Iterate over each job and get the number of applicants for that job
        for job in jobs:
            num_applicants = Application.query.filter_by(job_id=job.id).count()
            # Create a dictionary to store the job details and the number of applicants
            job_dict = {
                'company': job.company,
                'job_title': job.job_title,
                'job_category': job.job_category,
                'salary_range': job.salary_range,
                'number_of_applicants': num_applicants
            }
            # Append the job details to the list of job applications
            job_applications.append(job_dict)

        # Return the list of job applications as a JSON response
        return json.dumps(job_applications, default=str), 200


class JobApplication(Resource):

    def get(self, id):
        # Retrieve all applications submitted by the user with the given ID
        applications = Application.query.filter(Application.user_id == id).all()
        serialized_applications = []
        # Serialize the job ID of each application and append it to a list
        for application in applications:
            serialized_application = {
                'job_id': application.job_id
            }
            serialized_applications.append(serialized_application)
        # Return the list of serialized applications as a JSON response
        return json.dumps(serialized_applications, default=str), 200
    
    def delete(self, id):
        # Retrieve the application with the given job ID
        application = Application.query.filter(Application.job_id == id).first()
        # Return an error if the application is not found
        if not application:
            return {'message': 'Job application not found', 'status': 'error'}, 404
        # Delete the application from the database and commit the changes
        db.session.delete(application)
        db.session.commit()
        # Return a success message as a JSON response
        return {'message': 'Job application withdrawn successfully!', 'status': 'success'}, 200


class SingleJob(Resource):
    # Define a request parser for the job application endpoint
    applicant_job_parser = reqparse.RequestParser()
    applicant_job_parser.add_argument('id', type=int)
    applicant_job_parser.add_argument('closed', type=bool)

    # Get a single job by ID
    def get(self, id):
        # Query the database for the job with the specified ID
        job = Job.query.get(id)
        # Serialize the job object into a dictionary
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
        # Return the serialized job object as a JSON string
        return json.dumps(serialized_job, default=str), 200

    # Update a job by ID
    def put(self, id):
        # Query the database for the job with the specified ID
        job = Job.query.get(id)
        # Parse the request arguments
        data = SingleJob.applicant_job_parser.parse_args()
        # If the 'closed' field is provided, update the job status
        if data['closed']:
            job.closed = data['closed']
        # Add the job object to the session and commit the changes to the database
        db.session.add(job)
        db.session.commit()
        # Return a success message with the appropriate status code
        if data['closed']:
            return {'message': 'Job closed successfully!', 'status': 'success'}, 200
        return {'message': 'Job updated successfully!', 'status': 'success'}, 200

    # Apply for a job by ID
    def post(self, id):
        # Query the database for the job with the specified ID
        job = Job.query.get(id)
        # Parse the request arguments
        data = SingleJob.applicant_job_parser.parse_args()
        # Query the database for the user with the specified ID
        user = User.query.get(data)
        # Create a new application object and add it to the session
        application = Application(user=user, job=job)
        db.session.add(application)
        db.session.commit()
        # Return a success message with the appropriate status code
        return {'message': 'User successfully applied for the job', 'status': 'success'}, 200

class JobPosting(Resource):
    # create request parser for posting a new job
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
            # retrieve all non-closed jobs
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
            # return the list of serialized jobs in JSON format
            return json.dumps(serialized_jobs, default=str), 200
        except Exception as e:
            # if an error occurs, return a JSON object with the error message and 404 status code
            return jsonify({"error": str(e)}), 404
        
    def post(self):
        # parse the request data using the create_job_parser
        data = JobPosting.create_job_parser.parse_args()
        # create a new Job object with the parsed data
        new_job = Job(job_title = data['job_title'], salary_range = data['salary_range'], company = data['company'], job_category = data['job_category'], job_description = data['job_description'], email = data['email'], closed = data['closed'])
        # add the new Job object to the database session and commit the changes
        db.session.add(new_job)
        db.session.commit()
        # return a JSON object with a success message and 200 status code
        return {'message': 'Posted new job successfully!', 'status': 'success'}, 200
