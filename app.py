from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import openai
import pdfplumber
import io
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"I am Healthy App"}

@app.post("/upload/")
async def upload_files(cv: UploadFile = File(...), job_description: UploadFile = File(...)):
    """
    Accepts a CV and a job description, analyzes the CV in relation to the job description using OpenAI.

    Args:
        cv (UploadFile): The uploaded CV file.
        job_description (UploadFile): The uploaded job description file.
    
    Returns:
        JSONResponse: The result of the CV analysis or an error message in JSON format.
    """

    if cv.content_type not in ['application/pdf', 'text/plain'] or job_description.content_type not in ['application/pdf', 'text/plain']:
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload PDF or plain text files.")
    
    try:
        cv_text = await extract_text(cv)
        jd_text = await extract_text(job_description)
        result = analyze_documents(cv_text, jd_text)
        return JSONResponse(content={"analysis": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def extract_text(file: UploadFile) -> str:
    """
    Extracts and returns text from a PDF or plain text file.

    Args:
        file (UploadFile): The file to be processed.

    Returns:
        str: Text extracted from the file.
    """

    try:
        if file.content_type == 'application/pdf':
            with pdfplumber.open(io.BytesIO(await file.read())) as pdf:
                pages = [page.extract_text() for page in pdf.pages]
                text = " ".join(filter(None, pages))
                if text:
                    return text
                else:
                    raise ValueError("No text could be extracted from the PDF.")
        elif file.content_type == 'text/plain':
            return (await file.read()).decode('utf-8')
        else:
            raise ValueError("Unsupported file type. Please upload a PDF or plain text file.")
    except Exception as e:
        raise IOError(f"Failed to read the file: {str(e)}")



def analyze_documents(cv_text, jd_text):
    """
    Analyzes the CV text against the job description text using the OpenAI API.

    Args:
        cv_text (str): Text extracted from the CV file.
        jd_text (str): Text extracted from the job description file.

    Returns:
        str: A summary of how the CV matches the job description.
    """
    try:
        openai.api_key = os.getenv('OPENAI_API_KEY')  

        response = openai.ChatCompletion.create(
            model=os.getenv('MODEL_NAME', 'gpt-4-1106-preview'), 
            messages=[
                {"role": "system", "content": "You are an assistant who is expert in evaluating the CV according to job description."},
                {"role": "user", "content": f"""CV:\n{cv_text}\n\nJob Description:\n{jd_text}\n\n
                                                Task: Evaluate the candidate's CV against the Job Description to determine alignment between their qualifications, skills, and experiences with the job requirements.

                                                Matching Guidelines:
                                                    Field Relevancy:
                                                        Ensure the candidate's background is relevant to the Job Title.
                                                Review Process:
                                                    Review CV: Identify relevant experiences, skills, and qualifications.
                                                    Match Key Responsibilities: Compare candidate's past experiences with the job's responsibilities.
                                                    Evaluate Skills: Match skills on the CV with those in the Job Description, focusing on Skills alignment.
                                                    Assess Qualifications: Check educational background, certifications, and additional qualifications against job requirements but the candidate must not be over qualified.
                                                Scoring:
                                                    - Scale: 1 to 10
                                                    - Weightage:
                                                        - Skills: 40%
                                                        - Responsibilities Alignment: 40%
                                                        - Qualifications: 10%
                                                        - Others: 10%
                                                Scoring Rubric:
                                                    Poor Match (1-2): 10 to 20 precent alignment between CV and Job Description.
                                                    Moderate Match (3-4): 30 to 40 precent alignment between CV and Job Description.
                                                    Good Match (5-7):  50 to 70 precent alignment between CV and Job Description.
                                                    Excellent Match (8-9):  80 to 90 precent alignment between CV and Job Description.
                                                Response Format:
                                                    - Score: <score>
                                                    - Explanation: <Explanation of the score up to 4 lines>"""
                                                    }
            ],
            max_tokens=1000
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to process with OpenAI: {str(e)}")


