function formatExperimentName(experiment) {
  const names = {
    rabi: "Rabi Oscillation",
    f01_spectroscopy: "F01 Spectroscopy",
    t1: "T1 Relaxation",
    t2: "T2 Decoherence",
  };

  return names[experiment] || experiment;
}

function formatStatus(status) {
  if (!status) {
    return "UNKNOWN";
  }

  return status.toUpperCase();
}

function getStatusStyle(status) {
  const normalizedStatus =
    String(status || "").toLowerCase();

  const baseStyle = {
    display: "inline-block",
    padding: "5px 10px",
    borderRadius: "999px",
    fontSize: "0.78rem",
    fontWeight: "700",
    letterSpacing: "0.03em",
  };

  switch (normalizedStatus) {
    case "completed":
      return {
        ...baseStyle,
        background: "#e8f5e9",
        color: "#2e7d32",
      };

    case "running":
      return {
        ...baseStyle,
        background: "#fff8e1",
        color: "#f57f17",
      };

    case "queued":
      return {
        ...baseStyle,
        background: "#e3f2fd",
        color: "#1565c0",
      };

    case "failed":
      return {
        ...baseStyle,
        background: "#ffebee",
        color: "#c62828",
      };

    default:
      return {
        ...baseStyle,
        background: "#eeeeee",
        color: "#424242",
      };
  }
}

function formatTimestamp(timestamp) {
  if (!timestamp) {
    return "—";
  }

  const date = new Date(timestamp);

  if (Number.isNaN(date.getTime())) {
    return "Invalid date";
  }

  return date.toLocaleString();
}

function getParameterCount(parameters) {
  if (
    !parameters ||
    typeof parameters !== "object"
  ) {
    return 0;
  }

  return Object.keys(parameters).length;
}

function JobsTab({ jobs }) {
  if (!jobs || jobs.length === 0) {
    return (
      <div>
        <h2>Execution History</h2>

        <p>
          No experiment jobs are available yet.
        </p>

        <p>
          Run an experiment to create an execution
          record.
        </p>
      </div>
    );
  }

  // Create a copy so the original jobs array
  // from App.jsx is never mutated.
  const sortedJobs = [...jobs].sort(
    (a, b) => {
      const dateA =
        new Date(a.created_at).getTime();

      const dateB =
        new Date(b.created_at).getTime();

      return dateB - dateA;
    }
  );

  return (
    <div>
      <h2>Execution History</h2>

      <p>
        Experiment execution history and job status.
      </p>

      <div
        style={{
          marginTop: "20px",
          overflowX: "auto",
          border: "1px solid #ddd",
          borderRadius: "8px",
        }}
      >
        <table
          style={{
            width: "100%",
            minWidth: "760px",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr
              style={{
                background: "#fafafa",
              }}
            >
              <th
                style={{
                  textAlign: "left",
                  padding: "12px 14px",
                  borderBottom:
                    "2px solid #ddd",
                  fontSize: "0.85rem",
                  whiteSpace: "nowrap",
                }}
              >
                Job ID
              </th>

              <th
                style={{
                  textAlign: "left",
                  padding: "12px 14px",
                  borderBottom:
                    "2px solid #ddd",
                  fontSize: "0.85rem",
                }}
              >
                Experiment
              </th>

              <th
                style={{
                  textAlign: "left",
                  padding: "12px 14px",
                  borderBottom:
                    "2px solid #ddd",
                  fontSize: "0.85rem",
                }}
              >
                Status
              </th>

              <th
                style={{
                  textAlign: "left",
                  padding: "12px 14px",
                  borderBottom:
                    "2px solid #ddd",
                  fontSize: "0.85rem",
                }}
              >
                Parameters
              </th>

              <th
                style={{
                  textAlign: "left",
                  padding: "12px 14px",
                  borderBottom:
                    "2px solid #ddd",
                  fontSize: "0.85rem",
                }}
              >
                Created
              </th>
            </tr>
          </thead>

          <tbody>
            {sortedJobs.map((job) => (
              <tr
                key={job.job_id}
                style={{
                  transition:
                    "background 0.15s ease",
                }}
              >
                <td
                  style={{
                    padding: "12px 14px",
                    borderBottom:
                      "1px solid #eee",
                    fontFamily:
                      "monospace",
                    fontSize: "0.9rem",
                    whiteSpace: "nowrap",
                  }}
                >
                  {job.job_id}
                </td>

                <td
                  style={{
                    padding: "12px 14px",
                    borderBottom:
                      "1px solid #eee",
                    fontWeight: "500",
                    whiteSpace: "nowrap",
                  }}
                >
                  {formatExperimentName(
                    job.experiment
                  )}
                </td>

                <td
                  style={{
                    padding: "12px 14px",
                    borderBottom:
                      "1px solid #eee",
                  }}
                >
                  <span
                    style={getStatusStyle(
                      job.status
                    )}
                  >
                    {formatStatus(
                      job.status
                    )}
                  </span>
                </td>

                <td
                  style={{
                    padding: "12px 14px",
                    borderBottom:
                      "1px solid #eee",
                    color: "#555",
                  }}
                >
                  {getParameterCount(
                    job.parameters
                  )}
                </td>

                <td
                  style={{
                    padding: "12px 14px",
                    borderBottom:
                      "1px solid #eee",
                    whiteSpace: "nowrap",
                    color: "#555",
                  }}
                >
                  {formatTimestamp(
                    job.created_at
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p
        style={{
          marginTop: "12px",
          fontSize: "0.85rem",
          opacity: 0.65,
        }}
      >
        {sortedJobs.length}{" "}
        {sortedJobs.length === 1
          ? "job"
          : "jobs"}{" "}
        in execution history.
      </p>
    </div>
  );
}

export default JobsTab;