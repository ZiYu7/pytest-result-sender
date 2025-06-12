import requests

url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b1ba5bd9-029a-43ed-91e4-c1a2658f734f"

content = """
pytest自动化测试结果

测试时间：XXX-XXXX-XX <br/>
用例数量：100 <br/>
执行时长：50s <br/>
测试通过：<font color='green'>2 </font> <br/>
测试失败：<font color='red'>1 </font> <br/>
测试通过率：66.67% <br/>

测试报告地址：http://baidu.com
"""
response = requests.post(
    url, json={"msgtype": "markdown", "markdown": {"content": content}}
)
