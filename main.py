from typing import Optional
from DataModel import DataModel
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sklearn.base import BaseEstimator, TransformerMixin
from custom_transformers import preprocess_data

from joblib import load
import pandas as pd 

from custom_transformers import preprocess_data


app = FastAPI()

# Define a list of origins that should be allowed
# Use ["*"] to allow all origins
origins = [
    "http://localhost:3000",  
    "http://127.0.0.1:3000",
]

# Add middleware to support CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


pipeline = load('assets/proyecto1.joblib')

@app.get("/")
def read_root():
   return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
   return {"item_id": item_id, "q": q}

@app.post("/predict")
def make_predictions(data_model: DataModel):
    data_dict = data_model.dict()
    df = pd.DataFrame([data_dict], columns=data_model.columns())
    # df = preprocess_data(df)
    result = pipeline.predict(df['Review'])  # Ensure the model uses the correct input
    return {"result": result.tolist()}




@app.post("/upload-csv/")
async def upload_csv(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}, Content type: {file.content_type}")
    if file.content_type != 'text/csv':
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a CSV file."})

    try:

        # Read the CSV file directly into a DataFrame
        dataframe = pd.read_csv(file.file)
        
        dataframe = dataframe["Review"]

        # print(dataframe.head())
        # Preprocess the data
        preprocessed_data = preprocess_data(dataframe)

        predictions = pipeline.predict(preprocessed_data)  # Uncomment if prediction is needed

        # Return preprocessed data for verification
        return {
            # "file_size": file.size,
            # "data_preview": preprocessed_data.head().to_dict(),
            "predictions": predictions.tolist()  # Uncomment if prediction is needed
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "An error occurred while processing the file.", "error": str(e)})



