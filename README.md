# sustc-sakura-spider
## Requirements
- os
- random
- datetime
- requests
- bs4
## Application
- 爬取南科大教务系统的课程表信息并转存为ics文件。
- 在电脑或手机上打开ics文件可以把课程信息快速添加进日历app
## Usage
- 在根目录执行 ```python3 index.py```
- 双击```class.ics```。
## Change log
### v0.1.0 (2018-03-08 16:46:30 GMT+08:00)
- 能够登陆CAS系统获取JSESSIONID值
- 能够使用JSESSIONID值登陆教务系统爬取课程表并保存至本地的```class.ics```文件
