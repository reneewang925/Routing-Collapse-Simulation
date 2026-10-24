import json

# 打开你下载的 FinQA 数据
with open("test.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 提取前 50 条，把它们的背景文本拼成一个长文档，作为 KB
kb_data = []
for i, item in enumerate(data[:50]):
    # FinQA 的背景包含前置文本、表格、后置文本，我们把它们拼起来当做一个长文档
    pre_text = " ".join(item.get("pre_text", []))
    post_text = " ".join(item.get("post_text", []))
    table_text = str(item.get("table", [])) # 简单转为字符串
    
    # 组装成完整的背景段落
    full_context = f"Context: {pre_text} {post_text} Table Data: {table_text}"
    
    kb_data.append({
        "doc_id": f"finqa_doc_{i+1}",
        "text": full_context
    })

# 保存为 finqa_kb.json
with open("finqa_kb.json", "w", encoding="utf-8") as f:
    json.dump(kb_data, f, indent=2, ensure_ascii=False)

print("✅ 成功！已生成高风险知识库：finqa_kb.json，共", len(kb_data), "个文档块")