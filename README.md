
# 功能
1) 账号密码存储， 加密存储
2) 登录二次验证 MFA 
3) 主要模型： 
    密码组group：id user_id name icon    
    密码条目item: id name username password(加密存储) url comment
    自定义fields：id item_id key value
    日志logs: id user_id item_id verb content     
4) 菜单：
    密码管理
    操作日志
5) 双击复制密码\用户名\url

# TODO:
   1) 密码列表增加checkbox功能
   2) 优化fields页面显示，使用模态框
   3) 用户自助修改用户名密码及配置头像
   4) ~~同一个ip只能尝试登陆6次，不然就锁60分钟~~
   5) ~~操作日志~~
   6) ~~登陆审计，10分钟内3次失败则暂停访问~~
