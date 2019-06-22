# sustc-sakura-spider
## Requirements
- os
- random
- datetime
- requests
- bs4
## Application

- 爬取南科大教务系统的课程表信息并转存为ics文件。
- 在电脑或手机上打开ics文件可以把课程信息快速添加进日历app

## Usage

* 先在根目录执行 `python3 server.py`，看到 `Server started listening` 后**不要**关闭窗口

- 再在根目录执行 ```python3 interactive.py```
- 根据提示输入学号、密码、学期、学期起始日、开始周、结束周
- 运行完成后会在根目录下生成 `WeekXX-XX-of-XXXXXX.ics`
## Hints

* 如果想自动化此过程，可查看 `client.py` 了解详细请求逻辑
* 建议先试试单独取一周课表，确认无误后再尝试导入整个学期
* 对于某些奇怪的学期（例如国庆放假导致的某个教学周被跳过），需要分开两次生成，并对前后两段选取不同的学期起始日
* 执行过多可能导致 IP 被临时封禁，换 IP / 换电脑 / 等待10min 即可解封

## Change log

### v0.2.0 (2019-06-22 22:23:00 GMT+08:00)

> By nekonull (@jerrylususu)

* 域名从 `sustc` 更换为 `sustech`
* 重写了 `README.MD`
* 增加了交互式客户端
* 增加学期选择
* 增加多周支持
* 增加状态信息输出

### v0.1.0 (2018-03-08 16:46:30 GMT+08:00)

- 能够登陆CAS系统获取JSESSIONID值
- 能够使用JSESSIONID值登陆教务系统爬取课程表并保存至本地的```class.ics```文件