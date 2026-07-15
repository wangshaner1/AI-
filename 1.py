import threading
import time
from datetime import datetime

record_se = []
lock = threading.Lock()

class AIModel:
    name = ""
    model_type = ""
    def __init__(self,n,m):
        self.name = n
        self.model_type = m
    def predict(self, input_data):
        print(f"{self.name}模型收到输入：{input_data}，但具体推理逻辑由子类实现")
        pass

class TextModel(AIModel):
    def __init__(self,n,m):
        AIModel.__init__(self,n,m)
    def predict(self, input_data):
        print(f"文本模型{self.name}正在生成文本...")
        time.sleep(1)
        return f"生成的文本结果: {input_data}"

class ImageModel(AIModel):
    def __init__(self,n,m):
        AIModel.__init__(self,n,m)
    def predict(self, input_data):
        print(f"图像模型{self.name}正在识别图像...")
        time.sleep(1)
        return f"识别结果: {input_data}"

def user_request(user_name, model, input_data):
    start_time = datetime.now()
    result = model.predict(input_data)
    end_time = datetime.now()
    num = end_time - start_time
    t = {"user": user_name, "model": model.name, "cost": num,"result": result}
    lock.acquire()
    record_se.append(t)
    lock.release()


text_model = TextModel("GPT-4", "text")
image_model = ImageModel("ResNet50", "image")
requests = [
    ("A", text_model, "写一首诗"),
    ("B", text_model, "讲一个笑话"),
    ("C", image_model, "一张猫的图片"),
    ("D", image_model, "一张汽车的图片"),
]
threads = []

total_start = datetime.now()

for user, model, data in requests:
    t = threading.Thread(
        target=user_request,
        args=(user, model, data),
        name=user
    )
    threads.append(t)
for t in threads:
    t.start()
for t in threads:
    t.join()
total_end = datetime.now()
total_cost = total_end - total_start
for record in record_se:
    print(f"用户 {record['user']} 请求 {record['model']} 模型，"
          f"耗时 {record['cost']:} 秒，结果：{record['result']}")

print(f"\n总耗时（所有线程并发完成）: {total_cost:} 秒")