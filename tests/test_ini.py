import configparser
from pathlib import Path

import pytest

from pytest_result_sender import plugin

# fixture 'pytester' not found
pytest_plugins = "pytester"  # 告诉他我是测试开发


@pytest.fixture(autouse=True)
def mock():
    bak_data = plugin.data
    plugin.data = {
        "passed": 0,
        "failed": 0,
    }
    # 创建一个干净的测试环境
    yield
    # 恢复测试环境
    plugin.data = bak_data


# pytester（pytest 框架内置的测试工具，用于动态创建和执行测试文件）
# tmp_path（pytest 提供的临时目录路径，用于存放测试生成的临时文件）
@pytest.mark.parametrize("send_when", ["every", "on_fail"])
def test_send_when(send_when, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when = {send_when}
send_api = http://baidu.com
"""
    )

    # 断言：配置加载成功
    # config = pytest.parseconfig(config_path) 视频的案例
    # assert config.getini('send_when') == send_when
    parser = configparser.ConfigParser()
    parser.read(str(config_path))
    send_when_value = parser["pytest"]["send_when"]
    assert send_when_value == send_when

    pytester.makepyfile(  # 构造场景，测试全部通过
        """
        def test_pass():
            ...
        """
    )

    pytester.runpytest("-c", str(config_path))
    # 如何断言 插件有没有发送结果：
    print(plugin.data)
    if send_when == "every":
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None


@pytest.mark.parametrize("send_api", ["http://baidu.com", ""])
def test_send_api(send_api, pytester: pytest.Pytester, tmp_path: Path):
    config_path = tmp_path.joinpath("pytest.ini")
    config_path.write_text(
        f"""
[pytest]
send_when = every
send_api = {send_api}
    """
    )

    # 断言：配置加载成功
    # config = pytest.parseconfig(config_path) 视频的案例
    # assert config.getini('send_when') == send_when
    parser = configparser.ConfigParser()
    parser.read(str(config_path))
    send_api_value = parser["pytest"]["send_api"]
    assert send_api_value == send_api

    pytester.makepyfile(  # 构造场景，测试全部通过
        """
        def test_pass():
            ...
        """
    )

    pytester.runpytest("-c", str(config_path))
    # 如何断言 插件有没有发送结果：
    print(plugin.data)
    if send_api:
        assert plugin.data["send_done"] == 1
    else:
        assert plugin.data.get("send_done") is None
