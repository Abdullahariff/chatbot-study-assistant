 🎓 StudyBuddy - AI Computer Science Tutor

StudyBuddy is an AI-powered tutor designed to help university-level computer science students understand complex topics including Data Structures, Operating Systems, Machine Learning, Algorithms, DBMS, and Networks.

## 🚀 Features

- **📖 Topic Explanations**: Get clear explanations with commented code examples
- **❓ Interactive Quizzes**: Test your knowledge with multiple choice questions
- **💡 Study Tips**: Receive personalized study recommendations
- **🔖 Bookmarking**: Get suggestions on important topics to remember
- **💬 Chat Interface**: WhatsApp/Instagram-style professional chat UI

## 🛠️ Tech Stack

- **Backend**: FastAPI + Google Gemini AI
- **Frontend**: Streamlit
- **AI Model**: Google Gemini 2.5 Flash

## 📁 Project Structure

```
studybuddy/
├── backend/
│   ├── chatbot.py          # AI chatbot logic
│   └── .env                # Environment variables (not in repo)
├── frontend/
│   └── app.py              # Streamlit frontend
├── main.py                 # FastAPI server
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore file
└── README.md              # This file
```

## 🔧 Local Setup

### Prerequisites
- Python 3.8+
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/studybuddy.git
   cd studybuddy
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the `backend/` folder:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

5. **Run the backend server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Run the frontend (in another terminal)**
   ```bash
   cd frontend
   streamlit run app.py
   ```

## 🌐 Deployment on Streamlit Cloud

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 2: Deploy on Streamlit
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file path: `frontend/app.py`
5. Add secrets in Streamlit Cloud dashboard:
   - Key: `GEMINI_API_KEY`
   - Value: `your_actual_api_key`

### Step 3: Configure for Cloud Deployment
The app will automatically detect if it's running on Streamlit Cloud and adjust API endpoints accordingly.

## 📋 Usage Examples

**Topic Explanation:**
```
User: "Explain binary search with code"
StudyBuddy: Provides clear explanation with Python implementation
```

**Quiz Mode:**
```
User: "Quiz me on data structures"
StudyBuddy: Generates 3 MCQs with explanations
```

**Study Tips:**
```
User: "Give me study tips for algorithms"
StudyBuddy: Provides personalized study recommendations
```

## 🎯 Supported Topics

- Data Structures & Algorithms
- Operating Systems
- Database Management Systems (DBMS)
- Computer Networks
- Machine Learning
- Software Engineering Principles

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering the intelligent responses
- Streamlit for the amazing frontend framework
- FastAPI for the robust backend API

## 📞 Support

If you have any questions or run into issues, please open an issue on GitHub or contact the maintainers.

---

**Made with ❤️ for Computer Science Students**

---FILE_SEPARATOR---

# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration settings
class Config:
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Server Configuration
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # Streamlit Configuration
    IS_CLOUD = os.getenv("STREAMLIT_SHARING", False)
    
    @classmethod
    def get_backend_url(cls):
        """Get the appropriate backend URL based on environment"""
        if cls.IS_CLOUD:
            # For Streamlit Cloud deployment, we'll embed the backend
            return "http://localhost:8000"  # This will be adjusted for cloud
        return cls.BACKEND_URL
