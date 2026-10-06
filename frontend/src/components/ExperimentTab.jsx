function ExperimentTab({
  experiments,
  selectedExperiment,
  onExperimentChange,
  onRunExperiment,
  running,
}) {
  const selected = experiments.find(
    (experiment) => experiment.id === selectedExperiment
  );

  return (
    <div>
      <h2>Experiment</h2>

      <label>
        <strong>Select experiment:</strong>{" "}

        <select
          value={selectedExperiment}
          onChange={(event) =>
            onExperimentChange(event.target.value)
          }
        >
          {experiments.map((experiment) => (
            <option
              key={experiment.id}
              value={experiment.id}
            >
              {experiment.name}
            </option>
          ))}
        </select>
      </label>

      {selected && (
        <div>
          <p>
            <strong>Category:</strong>{" "}
            {selected.category}
          </p>

          <p>
            <strong>Status:</strong>{" "}
            {selected.status}
          </p>
        </div>
      )}

      <button
        onClick={onRunExperiment}
        disabled={running}
      >
        {running
          ? "Submitting..."
          : "Run Experiment"}
      </button>
    </div>
  );
}

export default ExperimentTab;