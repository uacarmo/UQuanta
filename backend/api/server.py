import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.api.parameter_validator import validate_parameters

#from backend.api.models import JobRequest, JobResponse
from backend.api.models import (
    JobRequest,
    JobResponse,
    ExperimentResult,
)

from backend.api.experiment_registry import (
    list_experiments,
    is_known_experiment,
)

from backend.api.job_manager import JobManager
from backend.api.experiment_runner import ExperimentRunner


app = FastAPI(
    title="Quantum Experiment, Calibration and Test Platform",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

job_manager = JobManager()
experiment_runner = ExperimentRunner()


@app.get("/api/v1/backend")
def backend_info():
    return {
        "name": "quantum_simulator",
        "version": "0.1.0",
        "status": "online",
        "type": "quantum_simulator",
        "capabilities": [
            "state_vector",
            "density_matrix",
            "hamiltonian_evolution",
            "lindblad_dynamics",
            "measurement",
        ],
    }


@app.get("/api/v1/experiments")
def get_experiments():
    return {
        "experiments": list_experiments()
    }


async def execute_job(job_id: str):
    """
    Execute a queued job in the background.
    """

    job = job_manager.get_job(job_id)

    if job is None:
        return

    try:
        job_manager.set_running(job_id)

        result = await asyncio.to_thread(
            experiment_runner.run,
            job.experiment,
            job.parameters,
        )

        job_manager.set_completed(
            job_id,
            result,
        )

    except Exception as exc:
        job_manager.set_failed(
            job_id,
            str(exc),
        )


@app.post("/api/v1/jobs", response_model=JobResponse)
async def create_job(request: JobRequest):

    if not is_known_experiment(request.experiment):
        raise HTTPException(
            status_code=400,
            detail=f"Unknown experiment: {request.experiment}",
        )

    try:
        validate_parameters(
            request.experiment,
            request.parameters,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        )

    job = job_manager.create_job(
        experiment=request.experiment,
        parameters=request.parameters,
    )

    asyncio.create_task(
        execute_job(job.job_id)
    )

    return {
        "job_id": job.job_id,
        "status": job.status,
    }


@app.get("/api/v1/jobs/{job_id}")
def get_job(job_id: str):

    job = job_manager.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "job_id": job.job_id,
        "experiment": job.experiment,
        "parameters": job.parameters,
        "status": job.status,
        "created_at": job.created_at,
        "result": job.result,
        "error": job.error,
    }

@app.get(
    "/api/v1/jobs/{job_id}/result",
    response_model=ExperimentResult,
)
def get_job_result(job_id: str):

    job = job_manager.get_job(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    if job.status == "queued":
        raise HTTPException(
            status_code=409,
            detail="Job is still queued",
        )

    if job.status == "running":
        raise HTTPException(
            status_code=409,
            detail="Job is still running",
        )

    if job.status == "failed":
        raise HTTPException(
            status_code=500,
            detail=job.error or "Job execution failed",
        )

    return job.result


@app.get("/api/v1/jobs")
def list_jobs():

    jobs = job_manager.list_jobs()

    return {
        "jobs": [
            {
                "job_id": job.job_id,
                "experiment": job.experiment,
                "parameters": job.parameters,
                "status": job.status,
                "created_at": job.created_at,
            }
            for job in jobs
        ]
    }