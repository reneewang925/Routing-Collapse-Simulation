# Mitigating Routing Collapse: Joint Optimization of Context Compression and Test-time Routing

This repository contains the code, n8n workflow, and dataset for the simulation of the "Routing Collapse" experiment. 

The project investigates the economic inflection point between context compression and test-time routing, incorporating a **Latency-aware Total Cost of Ownership (TCO)** model.

## 📂 Repository Structure
* `My workflow 1.json`: The complete n8n workflow architecture (includes LLMLingua, Qwen 1.5B, and Llama3 8B fallback logic).
* `llmlingua_api.py`: The FastAPI wrapper for the local LLMLingua compression service.
* `prepare_n8n_data.py` / `make_json.py`: Scripts used to generate and format the 50 test queries (FinQA and FAQ).
* `File (10).csv`: The final experimental results. *(Note: Includes granular token tracking for cheap/expensive models and precise latency metrics)*.
* `plot_results.py`: Python script to generate the Latency-aware TCO curve, Pareto Frontier, and Cost Breakdown charts.
* `Figure_1_TCO_with_latency.png` & `Figure_2_Pareto_latency.png`: The final plotted figures used in the poster.

## 🚀 How to Reproduce
1. Start the LLMLingua API: `uvicorn llmlingua_api:app --host 127.0.0.1 --port 8000`
2. Import `My workflow 1.json` into n8n.
3. Execute the n8n workflow to generate the raw CSV results.
4. Run `python plot_results.py` to generate the final figures.

## 📊 Key Findings
* **Routing Collapse in High-Risk Tasks:** For FinQA, extreme compression triggers Information Starvation, forcing frequent fallbacks to expensive models. The total TCO remains prohibitively high (>5000 units) due to double-paying for compute and latency.
* **Optimal Compression for Low-Risk Tasks:** FAQ tasks achieve a Pareto improvement at \(r=0.3\), balancing accuracy and cost.
* **The Latency Penalty:** Waiting time is modeled as an opportunity cost (\(P_{latency}\)), proving that unnecessary fallback routes destroy ROI in enterprise agentic workflows.
