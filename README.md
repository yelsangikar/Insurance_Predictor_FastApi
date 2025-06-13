🚀 Insurance Premium Prediction API + Streamlit Frontend
This project is a machine learning powered insurance premium category predictor built with:

🐍 FastAPI (backend API)

🎨 Streamlit (frontend UI)

🔒 JWT-based authentication (simple, file-based user storage)

📦 Optional Dockerization (for consistent deployment)

📌 Project Structure
bash
Copy
Edit
Insurance_Pred_FastApi/
├── main.py                  # FastAPI entrypoint
├── frontend.py               # Streamlit app
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (optional)
├── model/
│   ├── predict.py            # Prediction pipeline logic
│   ├── auth_utils.py         # JWT utilities + user storage
├── schema/
│   ├── user_input.py         # Input validation schemas
│   ├── prediction_response.py# Response model schema
├── config/
│   └── city_tier.py          # City tier mapping / config
├── users_db.json             # Local user store (auto-generated)
✨ Features
✅ Predict insurance premium category based on:

Age, Weight, Height

City tier

Income

Occupation

Smoker status

✅ JWT Auth

POST /register → Create user (saved to local JSON)

POST /login → Get JWT token

Secure predictions using token

✅ Streamlit frontend

Easy web UI for input + viewing results

✅ Ready for Docker / cloud deployment

⚙ How to run locally
1️⃣ Clone repo + install deps
bash
Copy
Edit
git clone <your-repo-url>
cd Insurance_Pred_FastApi
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
2️⃣ Run FastAPI server
bash
Copy
Edit
uvicorn main:app --reload
➡ Access API docs: http://127.0.0.1:8000/docs

3️⃣ Run Streamlit app
bash
Copy
Edit
streamlit run frontend.py
➡ Access UI: http://localhost:8501

🔑 Example auth flow
1️⃣ Register user:

bash
Copy
Edit
curl -X POST "http://127.0.0.1:8000/register?username=alice&password=pass123"
2️⃣ Login to get token:

bash
Copy
Edit
curl -X POST "http://127.0.0.1:8000/login?username=alice&password=pass123"
Response:

json
Copy
Edit
{
  "access_token": "<your_token_here>",
  "token_type": "bearer"
}
3️⃣ Use token in prediction requests:

http
Copy
Edit
Authorization: Bearer <your_token_here>
📦 Docker (optional)
Build
bash
Copy
Edit
docker build -t insurance-pred-api .
Run
bash
Copy
Edit
docker run -p 8000:8000 insurance-pred-api
🧪 Testing
👉 Future work — you can add unit tests with pytest:

nginx
Copy
Edit
pytest
(e.g. tests/test_predict.py, tests/test_auth.py)

🌐 Deployment (ideas)
✅ Railway / Render (PaaS)
✅ AWS EC2 + nginx
✅ Fly.io
✅ Heroku

📝 Notes
users_db.json is created/updated automatically when you register users.

Passwords are stored in plaintext for simplicity. In production, please use passlib or similar to hash + salt passwords.

The app currently runs locally; consider Docker or cloud hosting for deployment.

🤝 Contributing
Feel free to fork + PR enhancements!
Possible improvements:

Hash passwords

Add role-based access

Add tests

Improve Streamlit UI

🧑‍💻 Author
💡 Built by Chandan Kulkarni (2025)

📌 Quick links
API docs → http://127.0.0.1:8000/docs

Streamlit UI → http://localhost:8501

