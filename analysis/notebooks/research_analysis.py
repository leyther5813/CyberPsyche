"""
CyberPsyche — Decision-Process Laboratory for Social-Engineering Resilience
Statistical Research Analysis Package (Phase 5)

Analyzes exported researcher CSV data using pandas, scipy, statsmodels, and matplotlib.
"""

import os
import sys
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

def load_research_data(csv_path: str) -> pd.DataFrame:
    """Loads and preprocesses exported research CSV data."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Export CSV file not found at: {csv_path}")

    df = pd.read_csv(csv_path)

    # Clean boolean columns
    bool_cols = ["under_caution", "over_caution", "verified", "reason_alignment_flag"]
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().map({"true": True, "1": True, "1.0": True, "false": False, "0": False, "0.0": False}).fillna(False)

    # Clean numeric columns
    num_cols = ["confidence", "latency_ms", "decision_quality", "evidence_depth"]
    for col in num_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def calculate_hautus_sdt(malicious_df: pd.DataFrame, genuine_df: pd.DataFrame) -> dict:
    """Calculates Hautus (1995) log-linear corrected SDT metrics."""
    n_mal = len(malicious_df)
    n_gen = len(genuine_df)

    if n_mal == 0 or n_gen == 0:
        return {"hit_rate": 0.0, "false_alarm_rate": 0.0, "d_prime": 0.0, "criterion_c": 0.0}

    hits = sum(~malicious_df["under_caution"])  # Malicious scenario correctly defended
    false_alarms = sum(genuine_df["over_caution"])  # Genuine scenario incorrectly rejected

    h_adj = (hits + 0.5) / (n_mal + 1.0)
    fa_adj = (false_alarms + 0.5) / (n_gen + 1.0)

    z_h = float(stats.norm.ppf(h_adj))
    z_fa = float(stats.norm.ppf(fa_adj))

    d_prime = z_h - z_fa
    criterion_c = -0.5 * (z_h + z_fa)

    return {
        "hit_rate": round(hits / n_mal, 4),
        "false_alarm_rate": round(false_alarms / n_gen, 4),
        "d_prime": round(d_prime, 4),
        "criterion_c": round(criterion_c, 4),
    }

def generate_descriptive_stats(df: pd.DataFrame) -> pd.DataFrame:
    """Generates descriptive statistics matrix across study phases."""
    phases = ["baseline", "retest", "transfer"]
    records = []

    for ph in phases:
        ph_df = df[df["phase"] == ph]
        if ph_df.empty:
            continue

        mal_df = ph_df[ph_df["truth"] == "malicious"]
        gen_df = ph_df[ph_df["truth"] == "genuine"]
        sdt = calculate_hautus_sdt(mal_df, gen_df)

        records.append({
            "phase": ph,
            "count": len(ph_df),
            "verification_rate": round(ph_df["verified"].mean(), 4),
            "decision_quality_mean": round(ph_df["decision_quality"].mean(), 4),
            "under_caution_count": int(ph_df["under_caution"].sum()),
            "over_caution_count": int(ph_df["over_caution"].sum()),
            "evidence_depth_mean": round(ph_df["evidence_depth"].mean(), 4),
            "confidence_mean": round(ph_df["confidence"].mean(), 4),
            "latency_ms_mean": round(ph_df["latency_ms"].mean(), 1),
            "d_prime": sdt["d_prime"],
            "criterion_c": sdt["criterion_c"],
        })

    return pd.DataFrame(records)

def run_paired_analysis(df: pd.DataFrame) -> dict:
    """
    Performs paired statistical analysis (Wilcoxon signed-rank test) comparing:
    - Baseline vs Retest
    - Retest vs Transfer
    Decision Rule: Uses paired Wilcoxon signed-rank test due to bounded ordinal/ratio metrics.
    """
    results = {}
    pairs = [("baseline", "retest"), ("retest", "transfer")]

    for p1, p2 in pairs:
        g1 = df[df["phase"] == p1].groupby("session_id")
        g2 = df[df["phase"] == p2].groupby("session_id")

        for metric in ["verified", "decision_quality"]:
            v1 = g1[metric].mean()
            v2 = g2[metric].mean()
            common = v1.index.intersection(v2.index)

            if len(common) >= 5:
                diff = v2.loc[common] - v1.loc[common]
                if np.all(diff == 0):
                    stat, pval = 0.0, 1.0
                else:
                    stat, pval = stats.wilcoxon(v1.loc[common], v2.loc[common])
                
                # Effect size r = |Z| / sqrt(N)
                z_score = stats.norm.ppf(1 - pval / 2) if pval < 1 else 0.0
                effect_size = round(abs(z_score) / np.sqrt(len(common)), 4) if len(common) > 0 else 0.0

                results[f"{p1}_vs_{p2}_{metric}"] = {
                    "metric": metric,
                    "comparison": f"{p1} vs {p2}",
                    "n_participants": len(common),
                    "test": "Wilcoxon signed-rank test",
                    "statistic": float(stat),
                    "p_value": float(pval),
                    "effect_size_r": effect_size
                }
            else:
                results[f"{p1}_vs_{p2}_{metric}"] = {
                    "metric": metric,
                    "comparison": f"{p1} vs {p2}",
                    "n_participants": len(common),
                    "status": "Insufficient paired observations (n < 5)"
                }

    return results

def fit_mixed_effects_model(df: pd.DataFrame) -> dict:
    """
    Fits planned mixed-effects model: verified ~ phase * arm + pressure + (1|session_id) + (1|scenario_id)
    Handles singular fit / convergence issues gracefully.
    """
    if len(df) < 10:
        return {"status": "Model not estimable", "reason": "Insufficient sample size (n < 10)"}

    try:
        model = smf.mixedlm("verified ~ C(phase) * C(arm) + C(pressure)", df, groups=df["session_id"])
        fit_res = model.fit()
        return {
            "status": "Estimated successfully",
            "summary": str(fit_res.summary()),
            "aic": float(fit_res.aic) if hasattr(fit_res, "aic") else None,
            "params": fit_res.params.to_dict()
        }
    except Exception as e:
        return {"status": "Model failed to converge / singular fit", "reason": str(e)}

def run_pressure_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Produces descriptive performance comparison between low vs high pressure."""
    if "pressure" not in df.columns:
        return pd.DataFrame()

    records = []
    for press in ["low", "high"]:
        p_df = df[df["pressure"] == press]
        if p_df.empty:
            continue
        records.append({
            "pressure": press,
            "count": len(p_df),
            "verification_rate": round(p_df["verified"].mean(), 4),
            "decision_quality_mean": round(p_df["decision_quality"].mean(), 4),
            "under_caution_count": int(p_df["under_caution"].sum()),
            "over_caution_count": int(p_df["over_caution"].sum()),
        })
    return pd.DataFrame(records)

def run_mechanism_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Produces descriptive performance summary across social-engineering mechanisms."""
    if "mechanisms" not in df.columns:
        return pd.DataFrame()

    records = []
    # Explode mechanisms comma-separated strings
    mech_rows = []
    for _, row in df.iterrows():
        mechs = str(row["mechanisms"]).split(",")
        for m in mechs:
            m_clean = m.strip().upper()
            if m_clean and m_clean != "NAN":
                row_copy = row.to_dict()
                row_copy["mechanism_single"] = m_clean
                mech_rows.append(row_copy)

    mech_df = pd.DataFrame(mech_rows)
    if mech_df.empty:
        return pd.DataFrame()

    for m_name, group in mech_df.groupby("mechanism_single"):
        records.append({
            "mechanism": m_name,
            "count": len(group),
            "verification_rate": round(group["verified"].mean(), 4),
            "decision_quality_mean": round(group["decision_quality"].mean(), 4),
            "under_caution_count": int(group["under_caution"].sum()),
            "over_caution_count": int(group["over_caution"].sum()),
        })
    return pd.DataFrame(records)

def generate_plots(df: pd.DataFrame, output_dir: str):
    """Generates clean research-style academic plots using matplotlib."""
    os.makedirs(output_dir, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    # 1. Verification Rate by Phase
    phases = ["baseline", "retest", "transfer"]
    v_rates = [df[df["phase"] == ph]["verified"].mean() if not df[df["phase"] == ph].empty else 0.0 for ph in phases]
    
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(phases, [r * 100 for r in v_rates], color="#1e40af", width=0.5)
    ax.set_title("Independent Verification Rate by Phase", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Verification Rate (%)", fontsize=10)
    ax.set_ylim(0, 100)
    for i, v in enumerate(v_rates):
        ax.text(i, (v * 100) + 2, f"{v*100:.1f}%", ha="center", fontsize=9, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "verification_by_phase.png"), dpi=300)
    plt.close()

    # 2. Decision Quality by Phase
    dq_means = [df[df["phase"] == ph]["decision_quality"].mean() if not df[df["phase"] == ph].empty else 0.0 for ph in phases]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(phases, [dq * 100 for dq in dq_means], marker="o", color="#2563eb", linewidth=2.5, markersize=8)
    ax.set_title("Mean Decision Quality Across Phases", fontsize=12, fontweight="bold", pad=12)
    ax.set_ylabel("Decision Quality (%)", fontsize=10)
    ax.set_ylim(0, 100)
    for i, dq in enumerate(dq_means):
        ax.text(i, (dq * 100) + 3, f"{dq*100:.1f}%", ha="center", fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "decision_quality_by_phase.png"), dpi=300)
    plt.close()

    # 3. Verification by Pressure
    if "pressure" in df.columns:
        pressures = ["low", "high"]
        pv_rates = [df[df["pressure"] == pr]["verified"].mean() if not df[df["pressure"] == pr].empty else 0.0 for pr in pressures]
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(pressures, [r * 100 for r in pv_rates], color="#3b82f6", width=0.4)
        ax.set_title("Verification Rate by Social Pressure Level", fontsize=11, fontweight="bold", pad=12)
        ax.set_ylabel("Verification Rate (%)", fontsize=10)
        ax.set_ylim(0, 100)
        for i, v in enumerate(pv_rates):
            ax.text(i, (v * 100) + 2, f"{v*100:.1f}%", ha="center", fontsize=9)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, "verification_by_pressure.png"), dpi=300)
        plt.close()

    print(f"Academic research plots saved successfully to: {output_dir}")

def run_full_analysis(csv_path: str, output_dir: str = "analysis/reports"):
    """Main execution method for Phase 5 research analysis package."""
    print("=== CyberPsyche Statistical Research Analysis Package ===")
    df = load_research_data(csv_path)
    print(f"Loaded {len(df)} decision records from: {csv_path}\n")

    desc_df = generate_descriptive_stats(df)
    print("--- Phase Descriptive Statistics ---")
    print(desc_df.to_string(index=False))
    print("\n")

    paired = run_paired_analysis(df)
    print("--- Paired Analysis (Wilcoxon Signed-Rank Test) ---")
    for k, v in paired.items():
        print(f"{k}: {v}")
    print("\n")

    press_df = run_pressure_analysis(df)
    print("--- Pressure Analysis ---")
    print(press_df.to_string(index=False) if not press_df.empty else "No pressure data available")
    print("\n")

    mech_df = run_mechanism_analysis(df)
    print("--- Mechanism Vulnerability Analysis ---")
    print(mech_df.to_string(index=False) if not mech_df.empty else "No mechanism data available")
    print("\n")

    mem_res = fit_mixed_effects_model(df)
    print("--- Mixed-Effects Logistic Regression Model ---")
    print(f"Status: {mem_res['status']}")
    if "reason" in mem_res:
        print(f"Details: {mem_res['reason']}")
    print("\n")

    generate_plots(df, output_dir)
    print("=== Analysis Package Execution Completed Successfully ===")

if __name__ == "__main__":
    export_file = "analysis/data/cyberpsyche_research_export.csv"
    if not os.path.exists(export_file):
        export_file = "cyberpsyche_research_export.csv"
    
    if os.path.exists(export_file):
        run_full_analysis(export_file)
    else:
        print(f"Analysis script ready. Run with path to exported CSV: python analysis/notebooks/research_analysis.py <csv_path>")
