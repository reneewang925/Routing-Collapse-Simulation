import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", font_scale=1.2)
plt.rcParams['font.family'] = 'sans-serif'

# ==========================================
# 1. 读取数据
# ==========================================
# 注意：确保 File.csv 和这个脚本在同一个文件夹下，否则需要写绝对路径
df = pd.read_csv("File.csv", encoding="utf-8-sig")
df.columns = [c.strip() for c in df.columns]

numeric_cols = [
    'Rate', 'Latency_Seconds',
    'Cheap_Prompt_Tokens', 'Cheap_Output_Tokens', 
    'Fallback_Prompt_Tokens', 'Fallback_Output_Tokens'
]
for c in numeric_cols:
    df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)

df['Is_Correct_bool'] = df['Is_Correct'].astype(str).str.upper().str.strip().eq('TRUE')
df['Fallback_bool'] = df['Fallback_Triggered'].astype(str).str.upper().str.strip().isin(['YES', 'TRUE', '1'])

# 修复核心 Bug：原始长度 N 必须用未压缩时的 Cheap_Prompt_Tokens
n_mapping = (
    df[df['Rate'].eq(1.0)]
    .set_index(['Dataset', 'Query_ID'])['Cheap_Prompt_Tokens']
    .to_dict()
)

df['Original_Tokens_N'] = df.apply(
    lambda row: n_mapping.get(
        (row['Dataset'], row['Query_ID']),
        row['Cheap_Prompt_Tokens'] / row['Rate'] if row['Rate'] > 0 else row['Cheap_Prompt_Tokens']
    ),
    axis=1
)

# ==========================================
# 2. 单价设定 (经济学代理)
# ==========================================
P_cheap_in = 1.0    
P_cheap_out = 1.0   
P_exp_in = 15.0     
P_exp_out = 15.0    
P_compress = 0.1    

# 调大延迟单价，让延迟成本在图上显现 (设 1 秒 = 200 个 token 成本)
P_latency = 200.0

# ==========================================
# 3. 成本计算函数
# ==========================================
def add_costs(data, p_latency):
    d = data.copy()

    # A. 压缩成本：遍历原始 N
    d['Compress_Cost'] = d['Original_Tokens_N'] * P_compress

    # B. 小模型基础成本
    d['Cheap_Cost'] = (d['Cheap_Prompt_Tokens'] * P_cheap_in) + (d['Cheap_Output_Tokens'] * P_cheap_out)

    # C. 回退大模型算力惩罚 (直接用实际大模型的 Token)
    d['Fallback_Compute_Cost'] = (
        (d['Fallback_Prompt_Tokens'] * P_exp_in) + (d['Fallback_Output_Tokens'] * P_exp_out)
    )

    # D. 总计算成本
    d['Compute_TCO'] = d['Compress_Cost'] + d['Cheap_Cost'] + d['Fallback_Compute_Cost']

    # E. 延迟机会成本
    d['Latency_Cost'] = p_latency * d['Latency_Seconds']

    # F. 总 TCO
    d['TCO'] = d['Compute_TCO'] + d['Latency_Cost']

    return d

df = add_costs(df, P_latency)

# ==========================================
# 4. 汇总数据
# ==========================================
summary = df.groupby(['Dataset', 'Rate']).agg(
    Avg_Compute_TCO=('Compute_TCO', 'mean'),
    Avg_Latency_Cost=('Latency_Cost', 'mean'),
    Avg_TCO=('TCO', 'mean'),
    Accuracy=('Is_Correct_bool', 'mean'),
    Fallback_Rate=('Fallback_bool', 'mean')
).reset_index()

summary.to_csv("summary_latency_tco_v2.csv", index=False)

# 颜色设定
colors = {'FAQ_LowRisk': '#2ca02c', 'FinQA_HighRisk': '#d62728'}

# ==========================================
# 5. 画图 1：带延迟的 TCO 曲线 (折线图)
# ==========================================
plt.figure(figsize=(8, 5))
for dataset in summary['Dataset'].unique():
    subset = summary[summary['Dataset'] == dataset].sort_values('Rate', ascending=False)
    plt.plot(subset['Rate'], subset['Avg_TCO'], marker='o', linewidth=2.5, markersize=8, 
             label=f"{dataset}", color=colors[dataset])
    
    # 加上小圆点标注延迟成本和算力成本的比例
    for _, row in subset.iterrows():
        plt.text(row['Rate'], row['Avg_TCO'] + 50, f"FB:{row['Fallback_Rate']*100:.0f}%", 
                 ha='center', va='bottom', fontsize=9, color=colors[dataset])

plt.gca().invert_xaxis() 
plt.xlabel('Front-end Compression Rate (r)', fontsize=12, fontweight='bold')
plt.ylabel('Expected TCO incl. Latency (Relative Units)', fontsize=12, fontweight='bold')
plt.title('Latency-aware TCO vs Compression Rate', fontsize=14, fontweight='bold')
plt.legend(loc='upper center')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("Figure_1_TCO_with_latency_new.png", dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 6. 画图 2：帕累托前沿 (已修复 Y 轴截断问题)
# ==========================================
plt.figure(figsize=(10, 6))

# 1. 画出所有散点（不加虚线，只画点）
for dataset in summary['Dataset'].unique():
    subset = summary[summary['Dataset'] == dataset]
    plt.scatter(
        subset['Avg_TCO'], subset['Accuracy'], 
        s=150, color=colors[dataset], label=dataset, 
        edgecolors='white', linewidth=1.5, zorder=3
    )
    
    # 2. 在每个点旁边标注具体的 Rate 值
    for _, row in subset.iterrows():
        # 微调：如果点在 1.0 的高度，让文字往下偏一点，防止出界
        y_offset = -18 if row['Accuracy'] >= 0.99 else 6
        
        plt.annotate(
            f"r={row['Rate']}", 
            (row['Avg_TCO'], row['Accuracy']),
            textcoords="offset points", 
            xytext=(0, y_offset), 
            ha='center',
            fontsize=10, 
            fontweight='bold',
            color=colors[dataset]
        )

# 3. 计算全局帕累托前沿
def get_pareto_frontier(df, x_col, y_col, maximize_y=True):
    df_sorted = df.sort_values(by=[x_col, y_col], ascending=[True, not maximize_y])
    pareto_points = []
    max_y = -float('inf')
    
    for _, row in df_sorted.iterrows():
        if row[y_col] > max_y:
            pareto_points.append(row)
            max_y = row[y_col]
    return pd.DataFrame(pareto_points)

pareto_df = get_pareto_frontier(summary, 'Avg_TCO', 'Accuracy', maximize_y=True)

# 4. 绘制阶梯状的帕累托包络线
plt.plot(
    pareto_df['Avg_TCO'], pareto_df['Accuracy'], 
    color='grey', linestyle='-', linewidth=2.5, alpha=0.8, 
    label='Global Pareto Frontier', zorder=2,
    drawstyle='steps-post' 
)

plt.xlabel('Expected TCO incl. Latency (Relative Units)', fontsize=13, fontweight='bold')
plt.ylabel('Task Accuracy', fontsize=13, fontweight='bold')
plt.title('Pareto Frontier: Finding the Optimal Trade-off', fontsize=15, fontweight='bold')
plt.legend(loc='lower right', fontsize=11)
plt.grid(True, linestyle='--', alpha=0.5)

# 核心修复：Y轴上限改为 1.05，让准确率 1.0 的点浮现出来
plt.xlim(summary['Avg_TCO'].min() * 0.9, summary['Avg_TCO'].max() * 1.1)
plt.ylim(0.3, 1.05) 

plt.tight_layout()
plt.savefig("Figure_2_Pareto_Final_new.png", dpi=300, bbox_inches='tight')
plt.close()

# ==========================================
# 7. 画图 3：TCO 成本结构堆叠图
# ==========================================
finqa_sub = summary[summary['Dataset'] == 'FinQA_HighRisk'].sort_values('Rate', ascending=False)

plt.figure(figsize=(8, 5))
x = np.arange(len(finqa_sub))
width = 0.5

p1 = plt.bar(x, finqa_sub['Avg_Compute_TCO'], width, label='Compute OpEx', color='#1f77b4')
p2 = plt.bar(x, finqa_sub['Avg_Latency_Cost'], width, bottom=finqa_sub['Avg_Compute_TCO'], label='Latency Cost', color='#ff7f0e')

plt.xticks(x, [f"r={r}" for r in finqa_sub['Rate']])
plt.ylabel('Expected TCO', fontsize=12, fontweight='bold')
plt.title('TCO Cost Breakdown (FinQA_HighRisk)', fontsize=14, fontweight='bold')
plt.legend(loc='upper right')
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig("Figure_3_Cost_Breakdown_new.png", dpi=300, bbox_inches='tight')
plt.close()

print("✅ 所有图表与汇总数据已成功生成！")