# qichacha_spider
这是一个在企查查上收集备案信息的脚本，包括一个公司和它控股大于等于50%的子公司的有利于渗透测试的信息

R3_dev_anti_spider.py: 因为企查查更新了反爬虫机制，导致使用selemium打开的浏览器都无法爬取企查查的数据，因此使用了一些绕过方法。 使用此脚本的步骤如下： windows下，首先关闭所有chrome浏览器，并在任务管理器中关闭所有chrome的进程； 在cmd中输入："C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222，之后会看到chrome打开； chrome打开之后便可直接运行脚本了
