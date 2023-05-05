import os 
from app import create_app
from flask_restful import Api

from app.main.handle_jobs import Applicants, JobApplication, JobPosting, SingleJob

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

api=Api(app)    # create a new API object that is bound to the Flask app

# add resources to the API
api.add_resource(JobPosting, '/api/jobs')    # maps the JobPosting resource to the '/api/jobs' endpoint
api.add_resource(SingleJob, '/api/job/<int:id>')    # maps the SingleJob resource to the '/api/job/<id>' endpoint with a dynamic integer parameter
api.add_resource(JobApplication, '/api/application/<int:id>')    # maps the JobApplication resource to the '/api/application/<id>' endpoint with a dynamic integer parameter
api.add_resource(Applicants, '/api/applicants')    # maps the Applicants resource to the '/api/applicants' endpoint

if __name__ == '__main__':
    app.run(debug=True, port=5001)
