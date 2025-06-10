
from datetime import datetime

def pytest_configure():
    #配置加载完毕后执行，测试用例前执行

    print(f"{datetime.now()} pytest开始执行")

def pytest_unconfigure():
    # 配置加载完毕后执行，所有测试用例前执行

    print(f"{datetime.now()} pytest结束执行")
