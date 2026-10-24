import pandas as pd
import random

# 定义一些客服问题的模板
templates = [
    "How do I request a refund for my order?",
    "My package hasn't arrived yet, can you track it?",
    "I forgot my password, how do I reset it?",
    "Can I change the shipping address after placing the order?",
    "What is your return policy for electronics?",
    "How long does standard delivery take?",
    "I received a damaged item, what should I do?",
    "Do you offer discounts for bulk purchases?",
    "How can I cancel my subscription?",
    "Is there a customer service phone number I can call?"
]

# 生成 50 条（通过加前缀和组合）
queries = []
for i in range(50):
    prefix = random.choice(["Hi, ", "Hello, I need help. ", "Urgent: ", "Quick question: ", ""])
    # 循环使用模板
    base_q = templates[i % len(templates)]
    queries.append(prefix + base_q)

# 保存为 CSV
df_faq = pd.DataFrame({
    "Query_ID": range(1, 51),
    "Query_Text": queries
})

df_faq.to_csv("faq_queries_50.csv", index=False, encoding="utf-8-sig")
print("✅ 成功！已生成低风险客服数据集：faq_queries_50.csv")
print(df_faq.head())