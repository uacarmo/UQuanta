function formatLabel(name) {
  return name
    .replace(/_/g, " ")
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatNumber(value, digits = 4) {
  if (value === undefined || value === null) {
    return "—";
  }

  if (typeof value !== "number") {
    return String(value);
  }

  if (Math.abs(value) < 1e-12) {
    return "0.0000";
  }

  return value.toFixed(digits);
}

function formatPercent(value, digits = 4) {
  if (value === undefined || value === null) {
    return "—";
  }

  if (typeof value !== "number") {
    return String(value);
  }

  if (Math.abs(value) < 1e-12) {
    return "0.0000 %";
  }

  return `${value.toFixed(digits)} %`;
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

function StatusCard({
  passed,
  check = false,
  title,
  message,
}) {
  const statusText = check
    ? "✓ CHECK"
    : passed
      ? "✓ PASS"
      : "✗ FAIL";

  return (
    <div
      style={{
        border: "1px solid #ccc",
        borderRadius: "10px",
        padding: "20px",
        marginTop: "12px",
        marginBottom: "24px",
        background: "#fafafa",
      }}
    >
      <div
        style={{
          fontSize: "1.35rem",
          fontWeight: "700",
          marginBottom: "10px",
        }}
      >
        {statusText}
      </div>

      <div
        style={{
          fontSize: "1rem",
          fontWeight: "600",
          marginBottom: "8px",
        }}
      >
        {title}
      </div>

      <p
        style={{
          margin: 0,
          lineHeight: 1.5,
        }}
      >
        {message}
      </p>
    </div>
  );
}

function MetricGrid({ items }) {
  const visibleItems = items.filter(
    (item) =>
      item.value !== undefined &&
      item.value !== null
  );

  if (visibleItems.length === 0) {
    return null;
  }

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns:
          "repeat(auto-fit, minmax(180px, 1fr))",
        gap: "12px",
        marginBottom: "24px",
      }}
    >
      {visibleItems.map((item) => (
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
            {item.value}
          </div>
        </div>
      ))}
    </div>
  );
}

function CalibrationTab({ result }) {
  if (!result) {
    return (
      <div>
        <h2>Calibration</h2>

        <p>
          No calibration result available.
        </p>

        <p>
          Run an experiment to perform calibration
          analysis.
        </p>
      </div>
    );
  }

  const metadata = result.metadata || {};

  const experimentName =
    formatExperimentName(result.experiment);

  // -------------------------------------------------------
  // F01 Spectroscopy
  // -------------------------------------------------------
  if (result.experiment === "f01_spectroscopy") {
    const referenceF01 =
      metadata.f01 ??
      metadata.reference_frequency;

    const detectedResonance =
      metadata.resonance_frequency;

    const maximumProbability =
      metadata.maximum_probability ??
      metadata.max_excitation_probability;

    const relativeError =
      metadata.relative_error_percent ??
      metadata.frequency_error_percent;

    const tolerance = 1.0;

    const passed =
      relativeError !== undefined &&
      relativeError <= tolerance;

    return (
      <div>
        <h2>{experimentName} Calibration</h2>

        <p>
          Calibration of the qubit transition frequency
          using F01 spectroscopy.
        </p>

        <h3>Calibration Result</h3>

        <StatusCard
          passed={passed}
          title="Transition Frequency"
          message={
            passed
              ? "The detected resonance agrees with the reference transition frequency within the calibration tolerance."
              : "The detected resonance differs from the reference transition frequency by more than the allowed calibration tolerance."
          }
        />

        <h3>Frequency Analysis</h3>

        <MetricGrid
          items={[
            {
              label: "Reference F01",
              value: formatNumber(referenceF01),
            },
            {
              label: "Detected Resonance",
              value: formatNumber(
                detectedResonance
              ),
            },
            {
              label: "Frequency Error",
              value: formatPercent(
                relativeError
              ),
            },
            {
              label: "Tolerance",
              value: `${formatNumber(
                tolerance
              )} %`,
            },
            {
              label: "Maximum Excitation",
              value:
                maximumProbability !==
                undefined
                  ? `${(
                      maximumProbability * 100
                    ).toFixed(4)} %`
                  : undefined,
            },
          ]}
        />

        <h3>Calibration Criteria</h3>

        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "16px",
            background: "#fafafa",
          }}
        >
          <p style={{ marginTop: 0 }}>
            <strong>Acceptance criterion:</strong>
          </p>

          <p>
            Relative frequency error must be less
            than or equal to 1.0000 %.
          </p>

          <p
            style={{
              marginBottom: 0,
            }}
          >
            <strong>Measured error:</strong>{" "}
            {formatPercent(relativeError)}
          </p>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------
  // Rabi Oscillation
  // -------------------------------------------------------
  if (result.experiment === "rabi") {
    const xValues =
      result.data?.x?.values || [];

    const yValues =
      result.data?.y?.values || [];

    if (
      xValues.length < 3 ||
      yValues.length < 3
    ) {
      return (
        <div>
          <h2>{experimentName} Calibration</h2>

          <StatusCard
            passed={false}
            check
            title="Insufficient Data"
            message="The available Rabi data is insufficient for reliable peak and oscillation analysis."
          />
        </div>
      );
    }

    const maximumProbability =
      Math.max(...yValues);

    const minimumProbability =
      Math.min(...yValues);

    const amplitude =
      (maximumProbability -
        minimumProbability) /
      2;

    // -----------------------------------------------------
    // Find local maxima
    // -----------------------------------------------------
    const peakIndices = [];

    for (
      let i = 1;
      i < yValues.length - 1;
      i++
    ) {
      if (
        yValues[i] >= yValues[i - 1] &&
        yValues[i] >= yValues[i + 1]
      ) {
        peakIndices.push(i);
      }
    }

    // Only consider strong excitation maxima.
    const threshold =
      maximumProbability * 0.90;

    const significantPeaks =
      peakIndices.filter(
        (index) =>
          yValues[index] >= threshold
      );

    // -----------------------------------------------------
    // Quadratic interpolation
    // -----------------------------------------------------
    function interpolatePeak(index) {
      if (
        index <= 0 ||
        index >= yValues.length - 1
      ) {
        return {
          x: xValues[index],
          y: yValues[index],
        };
      }

      const x1 = xValues[index - 1];
      const x2 = xValues[index];
      const x3 = xValues[index + 1];

      const y1 = yValues[index - 1];
      const y2 = yValues[index];
      const y3 = yValues[index + 1];

      const dx = x2 - x1;

      const denominator =
        y1 - 2 * y2 + y3;

      if (
        Math.abs(denominator) < 1e-15
      ) {
        return {
          x: x2,
          y: y2,
        };
      }

      const offset =
        0.5 *
        (y1 - y3) /
        denominator;

      const peakX =
        x2 + offset * dx;

      const peakY =
        y2 -
        0.25 *
          (y1 - y3) *
          offset;

      return {
        x: peakX,
        y: peakY,
      };
    }

    // -----------------------------------------------------
    // First and second peaks
    // -----------------------------------------------------
    let firstPeak = null;
    let secondPeak = null;

    if (
      significantPeaks.length > 0
    ) {
      firstPeak =
        interpolatePeak(
          significantPeaks[0]
        );
    }

    if (
      significantPeaks.length > 1
    ) {
      secondPeak =
        interpolatePeak(
          significantPeaks[1]
        );
    }

    if (!firstPeak) {
      const maxIndex =
        yValues.indexOf(
          maximumProbability
        );

      firstPeak =
        interpolatePeak(maxIndex);
    }

    // -----------------------------------------------------
    // Rabi period
    // -----------------------------------------------------
    let rabiPeriod = null;

    if (secondPeak) {
      rabiPeriod =
        secondPeak.x -
        firstPeak.x;
    }

    const piPulseTime =
      firstPeak.x;

    // -----------------------------------------------------
    // Calibration criterion
    // -----------------------------------------------------
    const passed =
      maximumProbability >= 0.90 &&
      amplitude >= 0.40 &&
      significantPeaks.length >= 2;

    return (
      <div>
        <h2>{experimentName} Calibration</h2>

        <p>
          Calibration of coherent qubit control
          using the measured Rabi population
          oscillation.
        </p>

        <h3>Calibration Result</h3>

        <StatusCard
          passed={passed}
          check={!passed}
          title="Coherent Oscillation"
          message={
            passed
              ? "The Rabi response shows strong excitation and repeatable population maxima consistent with coherent oscillation."
              : "The Rabi response does not currently satisfy the initial calibration criteria."
          }
        />

        <h3>Signal Characteristics</h3>

        <MetricGrid
          items={[
            {
              label: "Number of Points",
              value: metadata.num_points,
            },
            {
              label: "Maximum Excitation",
              value: `${(
                maximumProbability * 100
              ).toFixed(4)} %`,
            },
            {
              label: "Minimum Excitation",
              value: `${(
                minimumProbability * 100
              ).toFixed(4)} %`,
            },
            {
              label: "Oscillation Amplitude",
              value: formatNumber(
                amplitude
              ),
            },
            {
              label: "Detected Peaks",
              value:
                significantPeaks.length,
            },
          ]}
        />

        <h3>Rabi Calibration Parameters</h3>

        <MetricGrid
          items={[
            {
              label: "First Maximum",
              value: formatNumber(
                firstPeak.x,
                6
              ),
            },
            {
              label:
                "First Maximum Probability",
              value: formatNumber(
                firstPeak.y,
                6
              ),
            },
            {
              label: "Second Maximum",
              value: secondPeak
                ? formatNumber(
                    secondPeak.x,
                    6
                  )
                : undefined,
            },
            {
              label:
                "Second Maximum Probability",
              value: secondPeak
                ? formatNumber(
                    secondPeak.y,
                    6
                  )
                : undefined,
            },
            {
              label: "Estimated Rabi Period",
              value: rabiPeriod
                ? formatNumber(
                    rabiPeriod,
                    6
                  )
                : undefined,
            },
            {
              label:
                "Estimated π-Pulse Time",
              value: formatNumber(
                piPulseTime,
                6
              ),
            },
          ]}
        />

        <h3>Calibration Criteria</h3>

        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "16px",
            background: "#fafafa",
          }}
        >
          <p style={{ marginTop: 0 }}>
            <strong>Acceptance criteria:</strong>
          </p>

          <p>
            Maximum excitation ≥ 90 %
          </p>

          <p>
            Oscillation amplitude ≥ 0.40
          </p>

          <p style={{ marginBottom: 0 }}>
            At least two significant excitation
            maxima must be detected.
          </p>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------
  // T1 Relaxation
  // -------------------------------------------------------
  if (result.experiment === "t1") {
    const referenceT1 =
      metadata.true_t1;

    const estimatedT1 =
      metadata.estimated_t1;

    const relativeError =
      metadata.relative_error_percent;

    const maximumTime =
      metadata.max_time;

    const slope =
      metadata.slope;

    const expectedSlope =
      referenceT1 !== undefined
        ? -1 / referenceT1
        : undefined;

    const tolerance = 1.0;

    const passed =
      relativeError !== undefined &&
      relativeError <= tolerance;

    return (
      <div>
        <h2>{experimentName} Calibration</h2>

        <p>
          Calibration of energy relaxation using
          the measured T1 decay curve.
        </p>

        <h3>Calibration Result</h3>

        <StatusCard
          passed={passed}
          title="Energy Relaxation Time"
          message={
            passed
              ? "The estimated T1 agrees with the reference relaxation time within the calibration tolerance."
              : "The estimated T1 differs from the reference relaxation time by more than the allowed calibration tolerance."
          }
        />

        <h3>Measurement Characteristics</h3>

        <MetricGrid
          items={[
            {
              label: "Number of Points",
              value: metadata.num_points,
            },
            {
              label: "Maximum Time",
              value: maximumTime,
            },
          ]}
        />

        <h3>T1 Calibration</h3>

        <MetricGrid
          items={[
            {
              label: "Reference T1",
              value: formatNumber(
                referenceT1
              ),
            },
            {
              label: "Estimated T1",
              value: formatNumber(
                estimatedT1
              ),
            },
            {
              label: "Relative Error",
              value: formatPercent(
                relativeError
              ),
            },
            {
              label: "Tolerance",
              value: `${formatNumber(
                tolerance
              )} %`,
            },
            {
              label: "Fitted Slope",
              value: formatNumber(
                slope
              ),
            },
            {
              label: "Expected Slope",
              value: formatNumber(
                expectedSlope
              ),
            },
          ]}
        />

        <h3>Calibration Criteria</h3>

        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "16px",
            background: "#fafafa",
          }}
        >
          <p style={{ marginTop: 0 }}>
            <strong>Acceptance criterion:</strong>
          </p>

          <p style={{ marginBottom: 0 }}>
            Relative T1 error must be less than or
            equal to 1.0000 %.
          </p>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------
  // T2 Coherence
  // -------------------------------------------------------
  if (result.experiment === "t2") {
    const referenceT2 =
      metadata.true_t2;

    const estimatedT2 =
      metadata.estimated_t2;

    const relativeError =
      metadata.relative_error_percent;

    const slope =
      metadata.slope;

    const intercept =
      metadata.intercept;

    const expectedSlope =
      referenceT2 !== undefined
        ? -1 / referenceT2
        : undefined;

    const tolerance = 1.0;

    const passed =
      relativeError !== undefined &&
      relativeError <= tolerance;

    return (
      <div>
        <h2>{experimentName} Calibration</h2>

        <p>
          Calibration of coherence decay using
          the measured T2 curve.
        </p>

        <h3>Calibration Result</h3>

        <StatusCard
          passed={passed}
          title="Coherence Time"
          message={
            passed
              ? "The estimated T2 agrees with the reference coherence time within the calibration tolerance."
              : "The estimated T2 differs from the reference coherence time by more than the 1% calibration tolerance."
          }
        />

        <h3>Measurement Characteristics</h3>

        <MetricGrid
          items={[
            {
              label: "Number of Points",
              value: metadata.num_points,
            },
            {
              label: "Maximum Time",
              value: metadata.max_time,
            },
            {
              label: "Measurement Shots",
              value: metadata.shots,
            },
            {
              label: "Random Seed",
              value: metadata.seed,
            },
          ]}
        />

        <h3>T2 Calibration</h3>

        <MetricGrid
          items={[
            {
              label: "Reference T2",
              value: formatNumber(
                referenceT2
              ),
            },
            {
              label: "Estimated T2",
              value: formatNumber(
                estimatedT2
              ),
            },
            {
              label: "Relative Error",
              value: formatPercent(
                relativeError
              ),
            },
            {
              label: "Tolerance",
              value: `${formatNumber(
                tolerance
              )} %`,
            },
            {
              label: "Fitted Slope",
              value: formatNumber(
                slope
              ),
            },
            {
              label: "Expected Slope",
              value: formatNumber(
                expectedSlope
              ),
            },
            {
              label: "Fitted Intercept",
              value: formatNumber(
                intercept
              ),
            },
          ]}
        />

        <h3>Calibration Criteria</h3>

        <div
          style={{
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "16px",
            background: "#fafafa",
          }}
        >
          <p style={{ marginTop: 0 }}>
            <strong>Acceptance criterion:</strong>
          </p>

          <p style={{ marginBottom: 0 }}>
            Relative T2 error must be less than or
            equal to 1.0000 %.
          </p>
        </div>
      </div>
    );
  }

  // -------------------------------------------------------
  // Other experiments
  // -------------------------------------------------------
  return (
    <div>
      <h2>{experimentName} Calibration</h2>

      <StatusCard
        passed={false}
        check
        title="Analysis Not Available"
        message="Calibration analysis for this experiment is not yet implemented."
      />
    </div>
  );
}

export default CalibrationTab;