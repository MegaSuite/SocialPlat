## TODO

- 用户jwt认证

## ✔️注册页面

> API 端点：http://social.caay.ru/api/register/

请求头：

- **Content-Type**: `application/json`

请求体：

```json
{
    "user_name": "用户姓名",
    "user_job": "用户专业",
    "user_contact": "用户联系方式",
    "user_password": "用户密码",
    "user_dob_year": "出生年份",
    "user_dob_month": "出生月份",
    "user_dob_day": "出生日",
    "user_gender": "性别",
    "user_custom_gender": "自定义性别",
    "user_hobbies": ["兴趣1", "兴趣2", ...]
}
```

响应体：

 ```json
 {
     "user_id": "用户的唯一标识符",
     "user_name": "用户姓名",
     "message": "Success"/"Failed"
 }
 ```



## ✔️登录页面

> API 端点：http://social.caay.ru/api/login/

请求头：

- **Content-Type**: `application/json`

请求体：

```json
{
    "user_contact": "用户联系方式",
    "user_password": "用户密码"
}
```

响应体：

```json
{
    "user_token": "your-authentication-token",
    "user_name": "用户姓名",
    "user_id": "用户的唯一标识符",
    "message": "Success"/"Failed"
}
```



## 论坛内容

> API端点：http://social.caay.ru/api/posts/

### 获取所有帖子

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

 请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "method": "all",
}
```

响应体：限制最大长度为20个帖子

```json
{
    "message": "Success"/"Failed",
    "posts":
    	[
        	{
                "post_id": "帖子的编号", 
                "post_author": "帖子的作者", 
                "post_title": "帖子的标题", 
                "post_content": "帖子的内容", 
                "post_comments": 
            		[
                    	{
                        	"comment_id": "评论的编号",
                            "comment_content": "评论的内容",
                            "comment_author": "评论的作者",
                        },
                    	{
                        	"comment_id": "评论的编号",
                            "comment_content": "评论的内容",
                            "comment_author": "评论的作者",
                        },
                    ]
            },
        	{
                "post_id": "帖子的编号", 
                "post_author": "帖子的作者", 
                "post_title": "帖子的标题", 
                "post_content": "帖子的内容", 
                "post_comments": 
            		[
                    	{
                        	"comment_id": "评论的编号",
                            "comment_content": "评论的内容",
                            "comment_author": "评论的作者",
                        },
                    	{
                        	"comment_id": "评论的编号",
                            "comment_content": "评论的内容",
                            "comment_author": "评论的作者",
                        },
                    ]
            },
        ],
}
```

### 发送帖子

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "post_title": "帖子的标题",
    "post_content": "帖子的内容",
    "method": "add",
}
```

响应体：

```json
{
    "post_id": "每篇帖子的唯一编号",
    "post_author": "帖子的作者",
    "message": "Success"/"Failed"
}
```

### 发送评论

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "post_id": "每篇帖子的唯一编号",
    "comment_content": "评论的内容",
    "method": "comment",
}
```

响应体：

```json
{
    "post_id": "每篇帖子的唯一编号",
    "post_author": "帖子的作者",
    "comment_id": "每条评论的唯一编号",
    "comment_author": "评论的作者",
    "message": "Success"/"Failed"
}
```



## 个人资料

>  API 端点：http://social.caay.ru/api/users/

### ✔️获取用户资料

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体： 

```json
{    
    "user_id": "用户的唯一标识符",
    "method": "request"
}
```

响应体：
```json
{
    "user_id": "用户的唯一标识符",
    "user_name": "用户姓名",
    "user_job": "用户专业",
    "user_contact": "用户联系方式",
    "user_password": "用户密码",
    "user_dob_year": "出生年份",
    "user_dob_month": "出生月份",
    "user_dob_day": "出生日",
    "user_gender": "性别",
    "user_custom_gender": "自定义性别",
    "user_hobbies": ["兴趣1", "兴趣2", "..."],
}
```

### ✔️更新用户资料

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "user_name": "用户姓名",
    "user_job": "用户专业",
    "user_contact": "用户联系方式",
    "user_password": "用户密码",
    "user_dob_year": "出生年份",
    "user_dob_month": "出生月份",
    "user_dob_day": "出生日",
    "user_gender": "性别",
    "user_custom_gender": "自定义性别",
    "user_hobbies": ["兴趣1", "兴趣2", "..."],
    "method": "renew"
}
```

响应体：

```json
{
    "user_id": "用户的唯一标识符",
    "user_name": "用户姓名",
    "message": "Success"/"Failed"
}
```

## 用户头像

> API 端点：http://social.caay.ru/api/avatar/

### 上传头像

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "avatar": "body",
    "method": "add"
}
```

响应体：

```json
{
    "avatar": "用户头像的URL",
    "message": "Success"/"Failed"
}
```

### 请求头像

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "method": "request"
}
```

响应体：

```json
{
    "avatar": "用户头像的URL",
    "message": "Success"/"Failed"
}
```

## 相似推荐

### 获取推荐好友列表 

> API 端点： http://social.caay.ru/api/recommend/

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
	"user_id": "当前登录用户的唯一标识符",
}
```

响应体：

```json
{
    "recommendations": 
    [
        {
            "user_id": "用户的唯一标识符",
            "user_name": "用户姓名",
            "user_job": "用户专业",
            "user_hobbies": ["兴趣1", "兴趣2", "..."],
            "avatar_url": "用户头像的URL"
        },
    ],
    "message": "Success" / "Failed"
}
```



## 好友关系

> API 端点： http://social.caay.ru/api/relation/

### 添加好友关系

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "当前登录用户的唯一标识符",
    "friend_add": "要添加的好友的用户ID"
    "method": "add",
}
```

响应体：

```json
{
    "user_id": "当前登录用户的唯一标识符",
    "friends": 
    	[
            {
                "id": "好友的用户ID",
                "name": "好友的姓名",
                "job": "好友的专业",
                "hobbies": ["好友的兴趣1", "好友的兴趣2", "..."]
            },
    	],
    "message": "Success" / "Failed"
}
```

### 查询好友关系

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "method": "request",
}
```

响应体：

```json
{
	"friends": 
    [
        {
            "id": "好友的用户ID",
            "name": "好友的姓名",
            "job": "好友的专业",
            "hobbies": ["好友的兴趣1", "好友的兴趣2", "..."]
        }
    ],
    "friendRequests": 
    [
        {
            "id": "好友请求用户ID",
            "name": "好友请求用户姓名"
        }
    ],
    "avatar": "用户头像的URL",
    "message": "Success"/"Failed"
}
```

### 响应好友请求

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "friend_request_id": "好友请求ID"
    "method": "Accept"/"Refuse"
}
```

响应体：

```json
{
    "friends": 
    [
        {
            "id": "好友的用户ID",
            "name": "好友的姓名",
            "job": "好友的专业",
            "hobbies": ["好友的兴趣1", "好友的兴趣2", "..."]
        }
    ],
    "message": "Success"/"Failed"
}
```
