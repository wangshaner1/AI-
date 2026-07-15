# 任务三代码
import time
import threading
from datetime import datetime 

#1.模型类
class AIModel:
    def __init__(self, name, model_type):
        self.name = name
        self.model_type = model_type

    def predict(self, input_data):
        raise NotImplementedError("子类必须实现predict方法")        

class TextModel(AIModel):
    def predict(self, input_data):
        # start = datetime.now()
        print(f"[{self.name}]正在生成文本：{input_data}")
        time.sleep(1)
        # end = datetime.now()
        # return {
        #     "output":f"《{input_data}》的生成结果",
        #     "cost":(end - start).totolseconds()            
        # }
        return f"文本结果：{input_data}"  

class ImageModel(AIModel):
    def predict(self, input_data):
        # start = datetime.now()
        print(f"[{self.name}]正在识别图像：{input_data}")
        time.sleep(1)
        # end = datetime.now()
        # return {
        #     "output":f"{input_data}的识别结果为：猫咪",
        #     "cost":(end - start).totolseconds()            
        # }
        return f"图像结果：{input_data}"

records = []
lock = threading.Lock()

def user_request(user_name, model, input_data):
        start = datetime.now()
        result = model.predict(input_data)
        end = datetime.now()
        cost = (end - start).total_seconds()

        lock.acquire()
        records.append({
            "user":user_name,
            "model":model.name,
            "cost":cost,
            "result":result        
        })
        lock.release()

text_model = TextModel("GPT小助手","文本生成")
image_model = ImageModel("图片识别器","文本生成")

total_start =  datetime.now()
threads = [
    threading.Thread(target=user_request, args=("用户A", text_model,"写首诗")),
    threading.Thread(target=user_request, args=("用户B", image_model,"cat.jpg")),
    threading.Thread(target=user_request, args=("用户C", text_model,"讲个笑话")),
]
for t in threads:
    t.start()
for t in threads:
    t.join()

total_end =  datetime.now()


print("\n=========请求明细=========")
for r in records:
    print(f"{r['user']}->{r['model']},耗时[{r['cost']}]:.2f秒，结果：[{r['result']}]")

print(f"\n总并发耗时：{(total_end - total_start).total_seconds():.2f}秒")