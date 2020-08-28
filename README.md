
# 功能
1) 账号密码存储， 加密存储
2) 登录二次验证 MFA -- 用户表加一个secret_key的字段
3) 模型： 
    群组group：id user_id name icon    
    条目item: id name username password(密码生成) url comment
    自定义key value customKV: id item_id key value
    日志logs: id user_id item_id verb content
     
4) 菜单：
    密码管理
    日志

# TODO:
   1 checkbox
   2 优化fields页面
   3 标签加icon功能
