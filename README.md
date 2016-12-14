# XcodeTargetCheck
检查Xcode项目的project文件中，target是否被人误删，并发送邮件告警

主要功能：
1.支持同时监测多个target
2.自动更新git，更新时间可以自己设置
3.支持多个邮件报警接收人
4.支持发送邮件时，带上target校验失败的列表，以及最近的git提交记录

参数配置：
所有参数在代码中都有详细注释，请按照规范配置即可。需要配置的参数都在代码的【全局变量区域】 。


邮件内容：【以下为示例】
2016-10-27 20:05:21:发生校验不合格事件。
被误删的tragte为:CJFTodayExtension1

git提交日志如下:
--------------------------------------------

[33mcommit c13df06e6871914179519f6bc4bd4d8fc45c5f73
Merge: 3700cb8 0629756
Author: 北京-xxxx <xxxx@xx.com>
Date:   Thu Oct 27 19:23:29 2016 +0800

    Merge branch 'sop' into dev

[33mcommit 0629756672c14c0409cc0d08026c4583bd507580
Author: 北京-xxxx <xxx@xx.com>
Date:   Thu Oct 27 19:21:40 2016 +0800

    sop已选择恢复

--------------------------------------------

