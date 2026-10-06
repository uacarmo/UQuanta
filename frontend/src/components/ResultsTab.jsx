import Plot from "react-plotly.js";

function formatLabel(name) {
  return name
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatNumber(value) {
  if (typeof value !== "number") {
    return String(value);
  }

  // Hide floating-point numerical noise
  if (Math.abs(value) < 1e-12) {
    return "0.0000";
  }

  if (Number.isInteger(value)) {
    return String(value);
  }

  return value.toFixed(4);
}

function formatMetadataValue(name, value) {
  if (typeof value !== "number") {
    return String(value);
  }

  // Integer-type metadata
  if (
    name === "num_points" ||
    name === "shots"
  ) {
    return String(Math.round(value));
  }

  // Percentage metadata
  if (
    name === "relative_error_percent" ||
    name === "frequency_error_percent"
  ) {
    if (Math.abs(value) < 1e-12) {
      return "0.0000 %";
    }

    return `${value.toFixed(4)} %`;
  }

  return formatNumber(value);
}

function formatExperimentName(experiment) {
  const names = {
    rabi: "Rabi Oscillation",
    f01_spectroscopy: "F01 Spectroscopy",
    t1: "T1 Relaxation",
    t2: "T2 Decoherence",
  };

  return names[experiment] || formatLabel(experiment);
}

function getSummaryItems(result) {
  const metadata = result.metadata || {};

  switch (result.experiment) {
    case "rabi":
      return [
        {
          label: "Number of Points",
          value: metadata.num_points,
        },
        {
          label: "Maximum Excitation",
          value:
            metadata.max_excitation_probability !== undefined
              ? `${(
                  metadata.max_excitation_probability * 100
                ).toFixed(4)} %`
              : undefined,
        },
        {
          label: "Rabi Period",
          value: metadata.estimated_rabi_period,
        },
        {
          label: "π-Pulse Time",
          value: metadata.estimated_pi_pulse_time,
        },
      ];

    case "f01_spectroscopy":
      return [
        {
          label: "Reference F01",
          value: metadata.reference_frequency,
        },
        {
          label: "Detected Resonance",
          value: metadata.resonance_frequency,
        },
        {
          label: "Frequency Error",
          value:
            metadata.frequency_error_percent !== undefined
              ? `${formatNumber(
                  metadata.frequency_error_percent
                )} %`
              : undefined,
        },
        {
          label: "Maximum Excitation",
          value:
            metadata.max_excitation_probability !== undefined
              ? `${(
                  metadata.max_excitation_probability * 100
                ).toFixed(4)} %`
              : undefined,
        },
      ];

    case "t1":
      return [
        {
          label: "Reference T1",
          value: metadata.true_t1,
        },
        {
          label: "Estimated T1",
          value: metadata.estimated_t1,
        },
        {
          label: "Relative Error",
          value:
            metadata.relative_error_percent !== undefined
              ? `${formatNumber(
                  metadata.relative_error_percent
                )} %`
              : undefined,
        },
        {
          label: "Fitted Slope",
          value: metadata.slope,
        },
      ];

    case "t2":
      return [
        {
          label: "Reference T2",
          value: metadata.true_t2,
        },
        {
          label: "Estimated T2",
          value: metadata.estimated_t2,
        },
        {
          label: "Relative Error",
          value:
            metadata.relative_error_percent !== undefined
              ? `${formatNumber(
                  metadata.relative_error_percent
                )} %`
              : undefined,
        },
        {
          label: "Fitted Slope",
          value: metadata.slope,
        },
      ];

    default:
      return [];
  }
}

function ResultsTab({ result }) {
  if (!result) {
    return (
      <div>
        <h2>Results</h2>
        <p>No experiment result available.</p>
        <p>
          Run an experiment to display the results here.
        </p>
      </div>
    );
  }

  const xValues = result.data?.x?.values || [];
  const yValues = result.data?.y?.values || [];

  const xName = result.data?.x?.name || "x";
  const xUnit = result.data?.x?.unit || "";

  const yName = result.data?.y?.name || "y";
  const yUnit = result.data?.y?.unit || "";

  const metadata = result.metadata || {};

  const resonance =
    metadata.resonance_frequency;

  const experimentName =
    formatExperimentName(result.experiment);

  const summaryItems =
    getSummaryItems(result);

  const hasData =
    xValues.length > 0 &&
    yValues.length > 0;

  const maxY =
    yValues.length > 0
      ? Math.max(...yValues)
      : 1;

  const yAxisRange =
    result.experiment === "rabi" ||
    result.experiment === "f01_spectroscopy"
      ? [0, 1]
      : undefined;

  return (
    <div>
      <h2>{experimentName}</h2>

      <p>
        <strong>Result Type:</strong>{" "}
        {result.result_type}
      </p>

      {summaryItems.some(
        (item) =>
          item.value !== undefined
      ) && (
        <>
          <h3>Summary</h3>

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit, minmax(180px, 1fr))",
              gap: "12px",
              marginBottom: "24px",
            }}
          >
            {summaryItems
              .filter(
                (item) =>
                  item.value !== undefined
              )
              .map((item) => (
                <div
                  key={item.label}
                  style={{
                    border: "1px solid #ddd",
                    borderRadius: "8px",
                    padding: "14px",
                    background: "#fafafa",
                  }}
                >
                  <div
                    style={{
                      fontSize: "0.85rem",
                      opacity: 0.7,
                      marginBottom: "6px",
                    }}
                  >
                    {item.label}
                  </div>

                  <div
                    style={{
                      fontSize: "1.15rem",
                      fontWeight: "600",
                    }}
                  >
                    {typeof item.value === "number"
                      ? formatNumber(item.value)
                      : item.value}
                  </div>
                </div>
              ))}
          </div>
        </>
      )}

      {hasData && (
        <>
          <h3>Experiment Data</h3>

          <Plot
            data={[
              {
                x: xValues,
                y: yValues,
                type: "scatter",
                mode: "lines",
                name: formatLabel(yName),
                line: {
                  width: 2,
                },
              },

              ...(resonance !== undefined
                ? [
                    {
                      x: [
                        resonance,
                        resonance,
                      ],
                      y: [0, maxY],
                      type: "scatter",
                      mode: "lines",
                      name: "Detected Resonance",
                      line: {
                        dash: "dash",
                        width: 2,
                      },
                    },
                  ]
                : []),
            ]}
            layout={{
              title: experimentName,

              xaxis: {
                title: xUnit
                  ? `${formatLabel(
                      xName
                    )} (${xUnit})`
                  : formatLabel(xName),
                zeroline: false,
              },

              yaxis: {
                title: yUnit
                  ? `${formatLabel(
                      yName
                    )} (${yUnit})`
                  : formatLabel(yName),
                range: yAxisRange,
                zeroline: false,
              },

              height: 500,

              margin: {
                l: 75,
                r: 30,
                t: 70,
                b: 70,
              },

              hovermode: "x unified",

              legend: {
                orientation: "h",
              },
            }}

            style={{
              width: "100%",
            }}

            useResizeHandler

            config={{
              responsive: true,
              displaylogo: false,
            }}
          />
        </>
      )}

      <h3>Metadata</h3>

      {Object.keys(metadata).length === 0 ? (
        <p>No metadata available.</p>
      ) : (
        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "16px",
            background: "#fafafa",
          }}
        >
          {Object.entries(metadata).map(
            ([name, value]) => (
              <div
                key={name}
                style={{
                  display: "flex",
                  justifyContent:
                    "space-between",
                  alignItems: "center",
                  gap: "20px",
                  padding: "7px 0",
                  borderBottom:
                    "1px solid #eee",
                }}
              >
                <strong>
                  {formatLabel(name)}
                </strong>

                <span>
                  {formatMetadataValue(
                    name,
                    value
                  )}
                </span>
              </div>
            )
          )}
        </div>
      )}
    </div>
  );
}

export default ResultsTab;
