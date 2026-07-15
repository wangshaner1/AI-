import time
import threading
from datetime import datetime

from concurrent.futures import ThreadPoolExecutor

# 1. 模型层
# 1.1 AI模型基类
class AIModel:
    def __init__(self, name, model_type):
        self.name = name
        self.model_type = model_type
    def predict(self, input_data):
        raise NotImplementedError("子类重写该方法实现功能")
    
# 1.2 文本模型
class TextModel(AIModel):
    def __init__(self, name, model_type):
        super().__init__(name, model_type)
    def predict(self, input_data):
        start = datetime.now()
        print(f"文本模型{self.name}正在生成文本...")
        time.sleep(1)
        end = datetime.now()
        cost = (end - start).total_seconds()
        return f"生成的文本结果: {input_data},耗时：{cost}秒"

# 1.3 图像模型
class ImageModel(AIModel):
    def __init__(self, name, model_type):
        super().__init__(name, model_type)
    def predict(self, input_data):
        start = datetime.now()
        print(f"图像模型{self.name}正在识别图像...")
        time.sleep(2)
        end = datetime.now()
        cost = (end - start).total_seconds()
        return f"图像识别结果: {input_data},耗时：{cost}秒"

'''
1. 新增语音模型 AudioModel，扩充任务列表
2. 将性能报表写入 report.txt
3. 用 ThreadPoolExecutor 实现线程池版本
'''
#语音模型
class AudioModel(AIModel):
    def __init__(self, name, model_type):
        super().__init__(name, model_type)
    def predict(self, input_data):
        start = datetime.now()
        print(f"语音模型{self.name}正在识别语音...")
        time.sleep(1.5)
        end = datetime.now()
        cost = (end - start).total_seconds()
        return f"语音识别结果: {input_data},耗时：{cost}秒"














# 2. 调度器 Scheduler
# 2.1 调度器基类
class Scheduler:
    def __init__(self):
        self.record = []#记录日志
        self.lock = threading.Lock()#创建锁
    def schedule(self, user_name, model, input_data):
        start = datetime.now()
        self.result = model.predict(input_data) # 调用模型预测
        end = datetime.now()
        self.cost = (end - start).total_seconds() # 计算耗时
        
# 2.2执行函数
    def _run_one(self, user_name, model, input_data):
        self.schedule(user_name, model, input_data) 
        self.lock.acquire() #获取锁
        self.record.append({"user":user_name,
                             "model":model.name, 
                             "input":input_data, 
                             "result":self.result, 
                             "cost":self.cost})   #记录日志
        self.lock.release() #释放锁
# 2.3 串行调度器
    def run_serial(self, requests):
        for user_name, model, input_data in requests:
            self._run_one(user_name, model, input_data)
# 2.4 并发调度器
    def run_concurrent(self, requests):
        threads = []   #创建线程列表
        for user_name, model, input_data in requests:
            t = threading.Thread(
                target=self._run_one,
                args=(user_name, model, input_data),
                name=user_name
            )        #创建线程
            threads.append(t)  #将线程添加到线程列表
        for t in threads:
            t.start()   #启动线程
        for t in threads:
            t.join()      #等待所有线程执行完毕


#线程池
    def run_pool(self, requests):
        with ThreadPoolExecutor(max_workers=5) as executor:
            threads = []   #创建线程列表
            for user_name, model, input_data in requests:
                t = executor.submit(self._run_one, user_name, model, input_data)
                threads.append(t)  #将线程添加到线程列表
            for t in threads:
                t.result()

#将性能报表写入 report.txt
def write_report(records,cost_1,cost_2,cost_3,filename="report.txt"):
    with open("report.txt", "w") as f:
        for record in records:
            f.write(f"用户 {record['user']} 请求 {record['model']} 模型，耗时 {record['cost']:} 秒，结果：{record['result']}\n")
        f.write(f"串行总耗时：{cost_1}秒\n")
        f.write(f"并发总耗时：{cost_2}秒\n")
        f.write(f"节省时长：{cost_1-cost_2}秒\n")
        f.write(f"并发比串行快了：{cost_1/cost_2}倍\n")
        f.write(f"线程池总耗时：{cost_3}秒\n")
    print(f"性能报表已写入 {filename}")





# 3. 主程序 main
if __name__ == "__main__":
    scheduler = Scheduler() #  创建模型
    text_model = TextModel("GPT-4", "text") #  创建文本模型
    image_model = ImageModel("豆包", "image") # 创建图像模型
    audio_model = AudioModel("小爱同学","audio")# 创建语音模型
    requests = [
        ("A", text_model, "写一段话"),
        ("B", image_model, "一张猫的图片"),
        ("C", text_model, "写一首诗"),
        ("D", image_model, "一张狗的图片"),
        ("E", text_model, "讲一个笑话"),
        ("F", image_model, "一张汽车的图片"),
        ("G", audio_model, "识别一段英语听力")
    ]                    #  创建请求
    start = datetime.now()
    scheduler.run_serial(requests) # 串行调度
    end = datetime.now()
    cost_1 = (end - start).total_seconds() #计算串行总时间


    start = datetime.now()
    scheduler.run_concurrent(requests)  # 并发调度
    end = datetime.now()
    cost_2 = (end - start).total_seconds()  #计算并发总时间

    start = datetime.now()
    scheduler.run_pool(requests)  # 线程池并发调度
    end = datetime.now()
    cost_3 = (end - start).total_seconds()  #计算并发总时间
    

    for record in scheduler.record:
        print(f"用户 {record['user']} 请求 {record['model']} 模型，耗时 {record['cost']:} 秒，结果：{record['result']}")#打印日志
    print(f"串行总耗时：{cost_1}秒")
    print(f"并发总耗时：{cost_2}秒")
    print(f"节省时长：{cost_1-cost_2}秒")
    print(f"并发比串行快了：{cost_1/cost_2}倍")
    print(f"线程池总耗时：{cost_3}秒\n")

    r = write_report(scheduler.record,cost_1,cost_2,cost_3)#将日志写入文件
    