# Joint Optimization of Context Compression and Test-Time Routing under Information Starvation

**Author:** Rui Wang  
**Supervisor:** Venketsh Viswanathan  
**Institution:** Stockholm University (DSV), SHAIO

## 📌 Overview
Agentic systems often face a compounding "Context Tax". While front-end context compression (e.g., LLMLingua) can reduce token costs, blind or extreme compression causes **Information Starvation**. This triggers **Routing Collapse**—a scenario where the system frequently falls back to expensive, large models (Llama3: 8B) but still fails to answer correctly.

This repository contains the experimental pipeline, raw data, and visualization scripts to evaluate the **Total Cost of Ownership (TCO)** under varying compression rates (\(r\)) and task risk levels (Low-Risk FAQ vs. High-Risk FinQA).

## 🔬 Key Findings
*   **FAQ (Low-Risk): Perfect Pareto Optimality.** Achieves 100% accuracy with a very low TCO (< 800 units) at \(r=1.0\) and \(r=0.8\). Over-compression (\(r<0.5\)) forces unnecessary fallbacks, increasing costs without any accuracy gains.
*   **FinQA (High-Risk): Severe Routing Collapse.** Information starvation triggers fallback rates to jump from 60% (\(r=1.0\)) to 80% (\(r=0.8\)). This causes a sharp TCO spike to **~3300** due to redundant compute and latency penalties. The absolute peak TCO (**~3600**) occurs at \(r=0.3\) where 100% fallback is forced.
*   **The "False Economy" of Extreme Compression:** At \(r=0.1\), although TCO slightly dips because the expensive model "gives up" and outputs extremely short rejection responses ("Not mentioned"), the task accuracy is permanently destroyed (drops to 40%). The entire frontend compression effort becomes pure **Sunk Cost**.

## ⚙️ Methodology
The Expected TCO is defined as a function of the compression rate \(r\):

$$
\mathbb{E}[TCO(r)] = \text{Compute OpEx} + \text{Latency Opportunity Cost}
$$

*   **Compute OpEx:** Includes the compression cost, the cheap model (Qwen2.5:1.5B) token costs, and the fallback large model (Llama3:8B) token costs.
*   **Latency Cost:** A penalty factor (1 second = 200 relative units) reflecting the opportunity cost of system waiting time.

### Experimental Pipeline
`Raw Data (FinQA / FAQ)` → `LLMLingua (Rate r)` → `Qwen2.5:1.5B (Cheap Inference)` → `Evaluator` → `Fallback to Llama3:8B (if triggered)`

## 📂 Code & Reproduction

```text
# Repository Structure
├── File.csv                         # Raw experimental data (50 queries, 5 compression rates)
├── plot_results.py                  # Python script to calculate TCO and generate all figures
├── Figure_1_TCO_with_latency.png    # Latency-aware TCO vs. Compression Rate
├── Figure_2_Pareto_Frontier.png     # Pareto Frontier (Task Accuracy vs. TCO)
├── Figure_3_Cost_Breakdown.png      # Stacked bar chart of Compute vs. Latency Costs
└── README.md                        # Project documentation


