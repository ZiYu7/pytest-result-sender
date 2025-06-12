from datetime import datetime

import pytest
import requests

data = {
    "passed": 0,
    "failed": 0,
}

def pytest_addoption(parser):
    parser.addini(
        'send_when',
        help="什么时候发送测试结果"
    )
    parser.addini(
        'send_api',
        help="结果发往何处"
    )

def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成之后执行，包含了全部的用例
    data["total"] = len(session.items)


def pytest_configure(config: pytest.Config):
    # 配置加载完毕后执行，测试用例前执行
    data["start_time"] = datetime.now()
    data["send_when"] = config.getini("send_when")
    data["send_api"] = config.getini("send_api")

def pytest_unconfigure():
    # 配置加载完毕后执行，所有测试用例前执行
    data["end_time"] = datetime.now()
    data["duration"] = data["end_time"] - data["start_time"]
    data["pass_ratio"] = data["passed"] / data["total"] * 100
    data["pass_ratio"] = f"{data['pass_ratio']:.2f}%"

    # assert timedelta(seconds=3)>= data['duration'] >=timedelta(seconds=2.5)
    # assert data['total'] == 3
    # assert data['passed'] == 2
    # assert data['failed'] == 1
    # assert data['pass_ratio'] == '66.67%'

    send_result()

def send_result():
    if data['send_when'] == 'on_fail' and data['failed'] == 0:
        #如果配置失败才发送，但实际没有失败，则不发送
        return
    if not data['send_api']:
        #如果没有配置api地址，则不发送
        print("api失败")
        return

    url = data['send_api'] #动态指定结果发送位置

    content = f"""
    pytest自动化测试结果

    测试时间：{data['end_time']} 
    用例数量：{data['total']} 
    执行时长：{data['duration']}
    测试通过：<font color='green'>{data['passed']}</font> 
    测试失败：<font color='red'>{data['failed']}</font> 
    测试通过率：{data['pass_ratio']} 

    测试报告地址：http://baidu.com
    """

    try:
        requests.post(url, json={"msgtype": "markdown",
                                 "markdown": {"content": content}})
    except Exception:
        pass
