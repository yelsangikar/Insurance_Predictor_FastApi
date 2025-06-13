from fastapi import FastAPI,HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from schema.user_input import UserInput, HomeResponse, HealthResponse
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION
from model.auth_utils import create_access_token, verify_token, users_db, save_users_db
from datetime import timedelta

app = FastAPI()

# human readable
@app.get('/', response_model=HomeResponse, tags=["General"], summary="Home", description="Welcome message for the Insurance Premium Prediction API.")
def home():
    return {'message': 'Insurance Premium Prediction API'}


# machine readable
@app.get('/health', response_model=HealthResponse)
def health_check(username: str = Depends(verify_token)):
    return {
        'status': 'OK',
        'version': MODEL_VERSION,
        'model_loaded': model is not None
    }

@app.post("/register")
def register(username: str, password: str):
    if username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    users_db[username] = password
    save_users_db()  # Save to file
    return {"msg": "User registered successfully"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    if username not in users_db or users_db[username] != password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": username},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}
@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput, username: str = Depends(verify_token)):
    user_input = {
        'bmi': data.bmi,
        'age_group': data.age_group,
        'lifestyle_risk': data.lifestyle_risk,
        'city_tier': data.city_tier,
        'income_lpa': data.income_lpa,
        'occupation': data.occupation
    }

    try:

        prediction = predict_output(user_input)

        return JSONResponse(status_code=200, content={'response': prediction})

    except Exception as e:

        return JSONResponse(status_code=500, content=str(e))