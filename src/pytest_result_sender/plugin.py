from datetime import datetime

import pytest
import requests

data = {
    "passed": 0,
    "failed": 0,
}


def pytest_runtest_logreport(report: pytest.TestReport):
    if report.when == "call":
        data[report.outcome] += 1


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成之后执行，包含了全部的用例
    data["total"] = len(session.items)


def pytest_configure():
    # 配置加载完毕后执行，测试用例前执行
    data["start_time"] = datetime.now()


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

    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b1ba5bd9-029a-43ed-91e4-c1a2658f734f"

    content = f"""
    pytest自动化测试结果

    测试时间：{data['end_time']} <br/>
    用例数量：{data['total']} <br/>
    执行时长：{data['duration']}s <br/>
    测试通过：<font color='green'>{data['passed']}</font> <br/>
    测试失败：<font color='red'>{data['failed']}</font> <br/>
    测试通过率：{data['pass_ratio']} <br/>

    测试报告地址：http://baidu.com
    """
    requests.post(url, json={"msgtype": "markdown", "markdown": {"content": content}})
