import os 
from app import create_app
from flask_migrate import Migrate
from flask_restful import Api

from app.main.handle_jobs import JobPosting, SingleJob

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
api=Api(app)
api.add_resource(JobPosting, '/api/jobs')
api.add_resource(SingleJob, '/api/job/<int:id>')

# migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
