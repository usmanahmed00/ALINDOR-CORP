## CV Screening Application
#### Streamlit is used to create frontend of application
#### FastApi is used to create backend APIs
#### How to run application:
- Visit this url: http://alindor-corp-1308189553.us-east-2.elb.amazonaws.com/
- Add your OpenAI key in " OpenAI Key " section of UI - For model, gpt-4 is used so key must support gpt-4!
- Upload your JD
- Upload your CV
- Click "Analyze" button
- You will get score + scoring details in response!

#### Additional points
- For frontend StreamLit is used because it's a lightweight Python library for fast development
- FastAPI is employed for creating efficient APIs on the backend
- For production, we can migrate application to advance frameworks like Reach and Next
- Application is dockerized for efficient dependencies management
- Deployed on AWS VM
