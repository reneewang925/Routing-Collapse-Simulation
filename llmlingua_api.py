from fastapi import FastAPI
from pydantic import BaseModel
from llmlingua import PromptCompressor

app = FastAPI()

print("正在加载 LLMLingua-2 模型，请稍候...")
# 关键修改1：必须添加 use_llmlingua2=True
compressor = PromptCompressor(
    model_name="microsoft/llmlingua-2-bert-base-multilingual-cased-meetingbank",
    use_llmlingua2=True, 
    device_map="cpu"
)

class Item(BaseModel):
    text: str
    rate: float
    
@app.post("/compress")
def compress(item: Item):
    try:
        # 文本太短直接返回，避免无意义的压缩
        if len(item.text.split()) < 10:
            return {"compressed_text": item.text}
            
        # 关键修改2：调用 LLMLingua-2 的专用方法
        result = compressor.compress_prompt_llmlingua2(
            item.text, 
            rate=item.rate,
            force_tokens=['\n', '.', '!', '?', ','], # 保留标点符号，避免语句粘连
            return_word_label=False
        )
        return {"compressed_text": result["compressed_prompt"]}
    except Exception as e:
        print(f"❌ 压缩失败: {e}")
        return {"compressed_text": item.text}