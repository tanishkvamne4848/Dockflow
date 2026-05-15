from fastapi import FastAPI
from pipeline.workflow import run_pipeline

app = FastAPI()


@app.get("/")
def home():
    return {"status": "DockFlow running"}


@app.post("/run")
def run(protein_path: str, ligand_path: str, output_dir: str = "dockflow_output", config_path: str = "config.yaml"):
    run_pipeline(protein_path=protein_path, ligand_path=ligand_path, output_dir=output_dir, config_path=config_path)
    return {"status": "Pipeline executed"}
