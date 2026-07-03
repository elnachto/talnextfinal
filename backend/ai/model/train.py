import os
import pickle
import warnings
import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report, accuracy_score
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.utils import shuffle
from sklearn.preprocessing import LabelEncoder

warnings.filterwarnings("ignore")

DATASET_PATH      = "datasets/cv_data.csv"
AREA_MODEL_PATH   = "ai/model/saved/area_model.pkl"
RANDOM_STATE      = 42
MIN_CLASS_SAMPLES = 2

df = pd.read_csv(DATASET_PATH)
df = df.dropna(subset=["text", "area", "seniority"])
df = df.drop_duplicates(subset=["text"])
df = shuffle(df, random_state=RANDOM_STATE)

area_counts = df["area"].value_counts()
valid_areas = area_counts[area_counts >= MIN_CLASS_SAMPLES].index
df = df[df["area"].isin(valid_areas)].copy()

print("\n=== DATASET INFO ===")
print(f"Total registros: {len(df)}\n")
print("Distribución por área:")
print(df["area"].value_counts())
print("\nDistribución por seniority:")
print(df["seniority"].value_counts())

X          = df["text"].astype(str)
y_area     = df["area"]
y_seniority = df["seniority"]

X_train_area, X_test_area, y_train_area, y_test_area = train_test_split(
    X, y_area,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y_area
)

X_train_sen, X_test_sen, y_train_sen, y_test_sen = train_test_split(
    X, y_seniority,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y_seniority
)

TFIDF_AREA = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    ngram_range=(1, 3),
    max_features=20_000,
    min_df=1,
    max_df=0.97,
    sublinear_tf=True,
    analyzer="word",
    token_pattern=r"(?u)\b[\w\.\+\#\-]+\b",
)

TFIDF_SEN = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    ngram_range=(1, 2),
    max_features=12_000,
    min_df=1,
    max_df=0.97,
    sublinear_tf=True,
    analyzer="word",
    token_pattern=r"(?u)\b[\w\.\+\#\-]+\b",
)

base_svc = LinearSVC(
    C=0.8,
    class_weight="balanced",
    max_iter=3000,
    random_state=RANDOM_STATE,
)

calibrated_svc = CalibratedClassifierCV(
    base_svc,
    cv=3,
    method="sigmoid",
)

area_pipeline = Pipeline([
    ("tfidf", TFIDF_AREA),
    ("clf",   calibrated_svc),
])

base_svc_sen = LinearSVC(
    C=1.0,
    class_weight="balanced",
    max_iter=3000,
    random_state=RANDOM_STATE,
)

calibrated_svc_sen = CalibratedClassifierCV(
    base_svc_sen,
    cv=3,
    method="sigmoid",
)

seniority_pipeline = Pipeline([
    ("tfidf", TFIDF_SEN),
    ("clf",   calibrated_svc_sen),
])

print("\n--- Entrenando área model ---")
area_pipeline.fit(X_train_area, y_train_area)
print("Área model listo.")

print("\n--- Entrenando seniority model ---")
seniority_pipeline.fit(X_train_sen, y_train_sen)
print("Seniority model listo.")
area_pred = area_pipeline.predict(X_test_area)
sen_pred  = seniority_pipeline.predict(X_test_sen)

print("\n=== ÁREA MODEL ===\n")
print(classification_report(y_test_area, area_pred, zero_division=0))
print(f"Accuracy: {round(accuracy_score(y_test_area, area_pred) * 100, 2)}%")

cv_scores = cross_val_score(
    area_pipeline, X, y_area,
    cv=StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE),
    scoring="accuracy",
)
print(f"CV Accuracy (5-fold): {round(cv_scores.mean() * 100, 2)}% ± {round(cv_scores.std() * 100, 2)}%")

print("\n=== SENIORITY MODEL ===\n")
print(classification_report(y_test_sen, sen_pred, zero_division=0))
print(f"Accuracy: {round(accuracy_score(y_test_sen, sen_pred) * 100, 2)}%")
os.makedirs("ai/model/saved", exist_ok=True)

with open(AREA_MODEL_PATH, "wb") as f:
    pickle.dump(area_pipeline, f)

SENIORITY_MODEL_PATH = "ai/model/saved/seniority_model.pkl"
with open(SENIORITY_MODEL_PATH, "wb") as f:
    pickle.dump(seniority_pipeline, f)

area_labels = list(area_pipeline.classes_)
with open("ai/model/saved/area_labels.pkl", "wb") as f:
    pickle.dump(area_labels, f)

print("\nModelos guardados en ai/model/saved/")

TESTS = [
    {
        "label": "Backend Junior",
        "text": "Junior backend developer. Node.js, Express, PostgreSQL. 1 year experience. REST APIs."
    },
    {
        "label": "Networking Mid",
        "text": "CCNA certified. Cisco routers and switches, VLANs, DHCP, DNS, routing protocols. 4 años administrando redes."
    },
    {
        "label": "Frontend Mid",
        "text": "Frontend developer 4 years. React, TypeScript, TailwindCSS. Next.js, Redux, performance optimization."
    },
    {
        "label": "DevOps Senior",
        "text": "Senior DevOps 8 years. Kubernetes, Terraform, AWS, CI/CD, Docker, Ansible. Led infra team of 6."
    },
    {
        "label": "SysAdmin Mid",
        "text": "Administrador Linux Ubuntu, VMware, Zabbix, Ansible. 5 años gestionando servidores en datacenter."
    },
    {
        "label": "Data Science Mid",
        "text": "Data scientist. Python, scikit-learn, pandas, XGBoost. Machine learning models for churn prediction."
    },
]

print("\n=== SMOKE TESTS ===\n")

for t in TESTS:
    area = area_pipeline.predict([t["text"]])[0]
    sen  = seniority_pipeline.predict([t["text"]])[0]
    proba       = area_pipeline.predict_proba([t["text"]])[0]
    classes     = area_pipeline.classes_
    top_idx     = np.argsort(proba)[::-1][:3]
    top_areas   = [(classes[i], round(float(proba[i]), 3)) for i in top_idx]
    print(f"[{t['label']}]")
    print(f"  Area:      {area}  |  Seniority: {sen}")
    print(f"  Top areas: {top_areas}")
    print("-" * 55)