# 🤖 AI Resume Analyzer (Django)

An intelligent web application that analyzes resumes against job descriptions using AI. It extracts skills, compares them with job requirements, and provides a score with improvement suggestions.

---

## 🚀 Features

* 📄 Upload resume (PDF format)
* 🧠 Extract skills from resume using text parsing
* 📌 Extract required skills from job description
* ⚖️ Compare resume skills with job requirements
* 📊 Generate match score (percentage)
* ✅ Show matching & missing skills
* 💡 Provide improvement suggestions using AI
* 🗂️ Store and view analysis history

---

## 🛠️ Tech Stack

* **Frontend:** HTML, CSS, Bootstrap
* **Backend:** Python, Django
* **Database:** SQLite / MySQL
* **Libraries:** PyPDF2, Regex
* **AI Integration:** OpenAI API

---

## 📂 Project Structure

```
AI_Resume_Analyzer/
│
├── analyzer/           # Main app
├── templates/          # HTML templates
├── static/             # CSS, JS files
├── media/              # Uploaded resumes
├── manage.py
├── db.sqlite3
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/sreejith5533/Ai-Resume-Analyzer-Full-Stack.git
cd ai-resume-analyzer
```

### 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Setup environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

### 5️⃣ Run migrations

```
python manage.py migrate
```

---

### 6️⃣ Start server

```
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

## 🧠 How It Works

1. User uploads resume (PDF)
2. System extracts text using PyPDF2
3. Skills are identified using Regex / AI
4. Job description is analyzed
5. AI compares both:

   * Matching skills
   * Missing skills
6. Score is calculated based on match percentage
7. Suggestions are generated to improve resume

---

## 📊 Output Example

* ✅ Matching Skills: Python, Django
* ❌ Missing Skills: React, REST API
* 📈 Score: 65%
* 💡 Suggestions:

  * Add missing technical skills
  * Improve project descriptions
  * Include measurable achievements

---

## ⚠️ Common Issues

* **API Quota Error (429)**
  → Check OpenAI billing & usage

* **Template Not Found Error**
  → Ensure templates folder is configured properly

* **File Upload Issues**
  → Check MEDIA_URL and MEDIA_ROOT settings

---

## 🔮 Future Improvements

* Resume parsing using NLP models
* ATS-friendly keyword optimization
* User authentication system
* Export analysis report (PDF)
* Dashboard with analytics

---

## 👨‍💻 Author

**Your Name**
Sreejith

---

