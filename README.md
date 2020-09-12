# check performance
 检查教务网成绩是否变更，发邮件提醒

## 目的
 目前已有校友提供了基于js的(成绩查询系统)[https://github.com/Vince-9/SWJTU-dean-score-crawler],因为只会玩python，所以这里提供一个基于python的解决方案

##使用
 1. 修改users_configs.txt的内容为“学号,密码,邮箱”，每行一个用户
 2. 使用计划任务程序（如windows计划任务，actions 或者云函数）定时执行“教务成绩提醒.py”脚本，间隔10分钟执行
 3. 当成绩跟新后，相应邮箱会收到提醒