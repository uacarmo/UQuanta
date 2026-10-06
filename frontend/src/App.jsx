import { useEffect, useState } from "react";

import TabBar from "./components/TabBar";
import ExperimentTab from "./components/ExperimentTab";
import ParametersTab from "./components/ParametersTab";
import ResultsTab from "./components/ResultsTab";
import CalibrationTab from "./components/CalibrationTab";
import JobsTab from "./components/JobsTab";

//const API_BASE_URL = "http://127.0.0.1:8000/api/v1";
const API_BASE_URL = "/api/v1";

function App() {
  // ----------------------------------------
  // Application state
  // ----------------------------------------

  const [experiments, setExperiments] = useState([]);
  const [selectedExperiment, setSelectedExperiment] = useState("");
  const [parameters, setParameters] = useState({});

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [jobId, setJobId] = useState(null);
  const [jobStatus, setJobStatus] = useState(null);
  const [running, setRunning] = useState(false);
  const [jobError, setJobError] = useState(null);

  const [result, setResult] = useState(null);
  const [jobs, setJobs] = useState([]);

  const [activeTab, setActiveTab] = useState("experiment");

  // ----------------------------------------
  // Load available experiments
  // ----------------------------------------

  useEffect(() => {
    async function loadExperiments() {
      try {
        setLoading(true);
        setError(null);

        const response = await fetch(
          `${API_BASE_URL}/experiments`
        );

        const data = await response.json();

        if (!response.ok) {
          throw new Error(
            data.detail || "Failed to load experiments"
          );
        }

        setExperiments(data.experiments || []);

        if (data.experiments?.length > 0) {
          setSelectedExperiment(data.experiments[0].id);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadExperiments();
  }, []);

  // ----------------------------------------
  // Load job history
  // ----------------------------------------

  useEffect(() => {
    fetchJobs();
  }, []);

  // ----------------------------------------
  // Selected experiment
  // ----------------------------------------

  const selected = experiments.find(
    (experiment) =>
      experiment.id === selectedExperiment
  );

  // ----------------------------------------
  // Load default parameters
  // ----------------------------------------

  useEffect(() => {
    if (!selected) {
      return;
    }

    const defaults = {};

    Object.entries(selected.parameters || {}).forEach(
      ([name, parameter]) => {
        defaults[name] = parameter.default;
      }
    );

    setParameters(defaults);
  }, [selected]);

  // ----------------------------------------
  // Parameter handling
  // ----------------------------------------

  function handleParameterChange(name, value) {
    setParameters((current) => ({
      ...current,
      [name]: value,
    }));
  }

  // ----------------------------------------
  // Run experiment
  // ----------------------------------------

  async function runExperiment() {
    if (!selectedExperiment) {
      setJobError("No experiment selected");
      return;
    }

    setRunning(true);
    setJobError(null);
    setJobId(null);
    setJobStatus(null);
    setResult(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/jobs`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            experiment: selectedExperiment,
            parameters: parameters,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to create job"
        );
      }

      setJobId(data.job_id);
      setJobStatus(data.status);

      // Wait for the job to finish.
      let finished = false;

      while (!finished) {
        await new Promise((resolve) =>
          setTimeout(resolve, 500)
        );

        finished = await checkJobStatus(data.job_id);
      }

      // Refresh job history after completion.
      await fetchJobs();

    } catch (err) {
      setJobError(err.message);
    } finally {
      setRunning(false);
    }
  }

  // ----------------------------------------
  // Check job status
  // ----------------------------------------

  async function checkJobStatus(id) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/jobs/${id}`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to get job status"
        );
      }

      setJobStatus(data.status);

      if (data.status === "completed") {
        await fetchJobResult(id);
        return true;
      }

      if (data.status === "failed") {
        setJobError(
          data.error || "Experiment failed"
        );

        return true;
      }

      return false;

    } catch (err) {
      setJobError(err.message);
      return true;
    }
  }

  // ----------------------------------------
  // Retrieve experiment result
  // ----------------------------------------

  async function fetchJobResult(id) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/jobs/${id}/result`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "Failed to get experiment result"
        );
      }

      setResult(data);

    } catch (err) {
      setJobError(err.message);
    }
  }

  // ----------------------------------------
  // Retrieve job history
  // ----------------------------------------

  async function fetchJobs() {
    try {
      const response = await fetch(
        `${API_BASE_URL}/jobs`
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to load jobs"
        );
      }

      setJobs(data.jobs || []);

    } catch (err) {
      setJobError(err.message);
    }
  }

  // ----------------------------------------
  // Loading state
  // ----------------------------------------

  if (loading) {
    return (
      <div className="app-workspace">
        <h1>
          UQuanta Measure and Calibration Platform
        </h1>

        <p>Loading experiments...</p>
      </div>
    );
  }

  // ----------------------------------------
  // Application error
  // ----------------------------------------

  if (error) {
    return (
      <div className="app-workspace">
        <h1>
          UQuanta Measure and Calibration Platform
        </h1>

        <p>
          <strong>Application error:</strong>{" "}
          {error}
        </p>

        <p>
          Make sure the FastAPI backend is running.
        </p>
      </div>
    );
  }

  // ----------------------------------------
  // Main application
  // ----------------------------------------

  return (
    <div className="app-workspace">

      <h1>
        UQuanta Measure and Calibration Platform
      </h1>

      {jobId && (
        <div className="job-status">
          <strong>Job:</strong> {jobId}
          {" — "}
          <strong>Status:</strong>{" "}
          {jobStatus || "unknown"}
        </div>
      )}

      {jobError && (
        <div className="job-error">
          <strong>Job error:</strong>{" "}
          {jobError}
        </div>
      )}

      <TabBar
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      <div className="workspace-content">

        {activeTab === "experiment" && (
          <ExperimentTab
            experiments={experiments}
            selectedExperiment={selectedExperiment}
            onExperimentChange={
              setSelectedExperiment
            }
            onRunExperiment={runExperiment}
            running={running}
          />
        )}

        {activeTab === "parameters" && (
          <ParametersTab
            selected={selected}
            parameters={parameters}
            onParameterChange={
              handleParameterChange
            }
          />
        )}

        {activeTab === "results" && (
          <ResultsTab result={result} />
        )}

        {activeTab === "calibration" && (
          <CalibrationTab result={result} />
        )}

        {activeTab === "jobs" && (
          <JobsTab jobs={jobs} />
        )}

      </div>
    </div>
  );
}

export default App;
