function ParametersTab({
  selected,
  parameters,
  onParameterChange,
}) {
  if (!selected) {
    return (
      <div>
        <h2>Parameters</h2>
        <p>No experiment selected.</p>
      </div>
    );
  }

  return (
    <div>
      <h2>Parameters</h2>

      <p>
        Parameters for{" "}
        <strong>{selected.name}</strong>
      </p>

      {Object.entries(selected.parameters).map(
        ([name, parameter]) => (
          <div key={name} style={{ marginBottom: "16px" }}>
            <label>
              <strong>{name}</strong>{" "}

              <input
                type="number"
                step={
                  parameter.type === "integer"
                    ? "1"
                    : "any"
                }
                min={parameter.minimum}
                value={parameters[name] ?? ""}
                onChange={(event) => {
                  const value =
                    parameter.type === "integer"
                      ? parseInt(
                          event.target.value,
                          10
                        )
                      : parseFloat(
                          event.target.value
                        );

                  onParameterChange(name, value);
                }}
              />

              {" "}
              <span>
                {parameter.unit}
              </span>
            </label>
          </div>
        )
      )}
    </div>
  );
}

export default ParametersTab;