from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class Job:
    job_id: str
    experiment: str
    parameters: dict[str, Any]
    status: str
    created_at: str
    result: Any | None = None
    error: str | None = None


class JobManager:

    def __init__(self):
        self._jobs: dict[str, Job] = {}
        self._counter = 0

    def create_job(
        self,
        experiment: str,
        parameters: dict[str, Any],
    ) -> Job:

        self._counter += 1

        job_id = f"job-{self._counter:06d}"

        job = Job(
            job_id=job_id,
            experiment=experiment,
            parameters=parameters,
            status="queued",
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        self._jobs[job_id] = job

        return job

    def get_job(self, job_id: str) -> Job | None:
        return self._jobs.get(job_id)

    def list_jobs(self) -> list[Job]:
        return list(self._jobs.values())

    def set_running(self, job_id: str) -> None:
        job = self._jobs.get(job_id)

        if job is None:
            raise ValueError(f"Job not found: {job_id}")

        job.status = "running"

    def set_completed(
        self,
        job_id: str,
        result: Any,
    ) -> None:

        job = self._jobs.get(job_id)

        if job is None:
            raise ValueError(f"Job not found: {job_id}")

        job.status = "completed"
        job.result = result
        job.error = None

    def set_failed(
        self,
        job_id: str,
        error: str,
    ) -> None:

        job = self._jobs.get(job_id)

        if job is None:
            raise ValueError(f"Job not found: {job_id}")

        job.status = "failed"
        job.error = error