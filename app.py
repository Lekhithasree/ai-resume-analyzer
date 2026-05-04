from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os
import PyPDF2

load_dotenv()

app = Flask(__name__)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

def extract_pdf_text(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

@app.route("/analyze", methods=["POST"])
def analyze():
    resume_file = request.files.get("resume_pdf")
    job_description = request.form.get("job_description", "")

    if not resume_file:
        return jsonify({"result": "Please upload a resume PDF."})

    resume_text = extract_pdf_text(resume_file)

    prompt = f"""
Analyze this resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Give:
1. Match percentage
2. Matching skills
3. Missing skills
4. Improvement suggestions
5. Improved resume bullet points
"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)

    return jsonify({"result": response.text})

if __name__ == "__main__":
    app.run(debug=True)

