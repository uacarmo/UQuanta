function TabBar({ activeTab, onTabChange }) {
  const tabs = [
    { id: "experiment", label: "Experiment" },
    { id: "parameters", label: "Parameters" },
    { id: "results", label: "Results" },
    { id: "calibration", label: "Calibration" },
    { id: "jobs", label: "Jobs" },
  ];

  return (
    <div className="tab-bar">
      {tabs.map((tab) => (
        <button
          key={tab.id}
          className={`tab-button ${
            activeTab === tab.id ? "active" : ""
          }`}
          onClick={() => onTabChange(tab.id)}
        >
          {tab.label}
        </button>
      ))}
    </div>
  );
}

export default TabBar;