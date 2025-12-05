"""
AI Data Science Research Assistant - FastAPI Backend
GPU-Accelerated ML Training with Full Feature Set
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import pandas as pd
import numpy as np
import json
import io
import os

# Import our modules
from app.ml_engine import MLEngine
from app.preprocessing import DataPreprocessor
from app.eda_engine import EDAEngine
from app.explainability import ModelExplainer

app = FastAPI(title="AI Data Science Assistant API", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage
datasets: Dict[str, pd.DataFrame] = {}
trained_models: Dict[str, Any] = {}
preprocessors: Dict[str, DataPreprocessor] = {}

# Initialize engines
ml_engine = MLEngine()
eda_engine = EDAEngine()

# ==================== MODELS ====================

class TrainRequest(BaseModel):
    dataset_id: str
    target_column: str
    task_type: str = "auto"
    use_gpu: bool = True
    hyperparameter_tuning: bool = False
    n_trials: int = 50
    cv_folds: int = 5
    test_size: float = 0.2

class PreprocessRequest(BaseModel):
    dataset_id: str
    handle_missing: str = "auto"  # auto, drop, mean, median, mode, knn
    handle_outliers: str = "none"  # none, clip, remove, winsorize
    encode_categorical: str = "auto"  # auto, onehot, label, target
    scale_features: str = "standard"  # none, standard, minmax, robust
    feature_selection: str = "none"  # none, correlation, variance, rfe

class PredictRequest(BaseModel):
    dataset_id: str
    model_id: str
    data: List[Dict[str, Any]]

# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    return {
        "name": "AI Data Science Assistant API",
        "version": "2.0.0",
        "gpu_available": ml_engine.gpu_available,
        "gpu_name": ml_engine.gpu_name
    }

@app.get("/health")
def health():
    return {"status": "healthy", "gpu": ml_engine.gpu_available}

# ==================== DATASET ENDPOINTS ====================

@app.post("/api/dataset/upload")
async def upload_dataset(file: UploadFile = File(...)):
    try:
        content = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(400, "Unsupported file format")
        
        dataset_id = f"ds_{len(datasets)}_{file.filename.split('.')[0]}"
        datasets[dataset_id] = df
        
        return {
            "id": dataset_id,
            "name": file.filename,
            "headers": df.columns.tolist(),
            "rows": df.head(100).to_dict('records'),
            "rowCount": len(df),
            "colCount": len(df.columns),
            "dtypes": df.dtypes.astype(str).to_dict()
        }
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/dataset/{dataset_id}")
def get_dataset(dataset_id: str, rows: int = 100):
    if dataset_id not in datasets:
        raise HTTPException(404, "Dataset not found")
    
    df = datasets[dataset_id]
    return {
        "id": dataset_id,
        "headers": df.columns.tolist(),
        "rows": df.head(rows).to_dict('records'),
        "rowCount": len(df),
        "colCount": len(df.columns)
    }

@app.get("/api/dataset/list")
def list_datasets():
    return [
        {"id": k, "rows": len(v), "cols": len(v.columns)}
        for k, v in datasets.items()
    ]

# ==================== PREPROCESSING ENDPOINTS ====================

@app.post("/api/preprocess")
def preprocess_data(request: PreprocessRequest):
    if request.dataset_id not in datasets:
        raise HTTPException(404, "Dataset not found")
    
    df = datasets[request.dataset_id].copy()
    preprocessor = DataPreprocessor()
    
    result = preprocessor.fit_transform(
        df,
        handle_missing=request.handle_missing,
        handle_outliers=request.handle_outliers,
        encode_categorical=request.encode_categorical,
        scale_features=request.scale_features,
        feature_selection=request.feature_selection
    )
    
    # Store preprocessed data
    new_id = f"{request.dataset_id}_processed"
    datasets[new_id] = result['data']
    preprocessors[new_id] = preprocessor
    
    return {
        "dataset_id": new_id,
        "original_shape": df.shape,
        "new_shape": result['data'].shape,
        "transformations": result['transformations'],
        "removed_columns": result.get('removed_columns', []),
        "encoded_columns": result.get('encoded_columns', {}),
        "scaling_params": result.get('scaling_params', {})
    }

@app.get("/api/preprocess/options")
def get_preprocessing_options():
    return {
        "handle_missing": ["auto", "drop", "mean", "median", "mode", "knn", "iterative"],
        "handle_outliers": ["none", "clip", "remove", "winsorize", "isolation_forest"],
        "encode_categorical": ["auto", "onehot", "label", "target", "binary", "frequency"],
        "scale_features": ["none", "standard", "minmax", "robust", "maxabs", "quantile"],
        "feature_selection": ["none", "correlation", "variance", "rfe", "mutual_info", "lasso"]
    }

# ==================== EDA ENDPOINTS ====================

@app.post("/api/eda/analyze")
def run_eda(dataset_id: str):
    if dataset_id not in datasets:
        raise HTTPException(404, "Dataset not found")
    
    df = datasets[dataset_id]
    results = eda_engine.full_analysis(df)
    return results

@app.post("/api/eda/statistical-tests")
def statistical_tests(dataset_id: str, column1: str, column2: Optional[str] = None):
    if dataset_id not in datasets:
        raise HTTPException(404, "Dataset not found")
    
    df = datasets[dataset_id]
    results = eda_engine.statistical_tests(df, column1, column2)
    return results

# ==================== ML TRAINING ENDPOINTS ====================

@app.post("/api/ml/train")
def train_models(request: TrainRequest):
    if request.dataset_id not in datasets:
        raise HTTPException(404, "Dataset not found")
    
    df = datasets[request.dataset_id]
    
    if request.target_column not in df.columns:
        raise HTTPException(400, f"Target column '{request.target_column}' not found")
    
    results = ml_engine.train_all_models(
        df=df,
        target_column=request.target_column,
        task_type=request.task_type,
        use_gpu=request.use_gpu,
        hyperparameter_tuning=request.hyperparameter_tuning,
        n_trials=request.n_trials,
        cv_folds=request.cv_folds,
        test_size=request.test_size
    )
    
    # Store trained models
    model_id = f"model_{request.dataset_id}_{request.target_column}"
    trained_models[model_id] = results['best_model']
    
    return results

@app.get("/api/ml/gpu-status")
def gpu_status():
    return ml_engine.get_gpu_status()

# ==================== EXPLAINABILITY ENDPOINTS ====================

@app.post("/api/explain/shap")
def get_shap_values(dataset_id: str, model_id: str, num_samples: int = 100):
    if model_id not in trained_models:
        raise HTTPException(404, "Model not found")
    if dataset_id not in datasets:
        raise HTTPException(404, "Dataset not found")
    
    model = trained_models[model_id]
    df = datasets[dataset_id]
    
    explainer = ModelExplainer(model)
    shap_results = explainer.compute_shap(df.head(num_samples))
    
    return shap_results

@app.post("/api/explain/feature-importance")
def get_feature_importance(model_id: str):
    if model_id not in trained_models:
        raise HTTPException(404, "Model not found")
    
    model = trained_models[model_id]
    explainer = ModelExplainer(model)
    
    return explainer.get_feature_importance()

# ==================== PREDICTION ENDPOINTS ====================

@app.post("/api/predict")
def predict(request: PredictRequest):
    if request.model_id not in trained_models:
        raise HTTPException(404, "Model not found")
    
    model_data = trained_models[request.model_id]
    df = pd.DataFrame(request.data)
    
    # Apply preprocessing if available
    if request.dataset_id in preprocessors:
        df = preprocessors[request.dataset_id].transform(df)
    
    predictions = model_data['model'].predict(df)
    
    result = {"predictions": predictions.tolist()}
    
    # Add probabilities for classification
    if hasattr(model_data['model'], 'predict_proba'):
        probas = model_data['model'].predict_proba(df)
        result["probabilities"] = probas.tolist()
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
