## 注册页面

> API 端点：http://23.184.88.52:8000/api/register/

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

 

## 登录页面

> API 端点：http://23.184.88.52:8000/api/login/

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
  "message": "Success"/"Failed"
}
```



## 个人资料

> API 端点：http://23.184.88.52:8000/api/users/

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
}
```

 响应体：

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



 ## 好友关系

> API端点：http://23.184.88.52:8000/api/relation/

### 添加好友关系

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "method": "add",
    “friend_add": "要添加的好友的唯一标识符"
}
```

响应体：返回更新后的好友列表

```json
{
	"user_id": "用户的唯一标识符"
 	"friends": 
    [
    	{ 
    		"id": 2, 
    		"name": "李三", 
    		"job": "信息技术", 
    		"hobbies": ["编程", "音乐"] 
		},
  		{ 
            "id": 3, 
            "name": "李二", 
            "job": "信息技术", 
            "hobbies": ["旅行", "音乐"] 
        },
  		{ 
            "id": 4, 
            "name": "李四", 
            "job": "信息技术", 
            "hobbies": ["旅行", "音乐"] 
        }
	]
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
	"user_id": "用户的唯一标识符"
 	"friends": 
    [
    	{ 
    		"id": 2, 
    		"name": "李三", 
    		"job": "信息技术", 
    		"hobbies": ["编程", "音乐"] 
		},
  		{ 
            "id": 3, 
            "name": "李二", 
            "job": "信息技术", 
            "hobbies": ["旅行", "音乐"] 
        },
  		{ 
            "id": 4, 
            "name": "李四", 
            "job": "信息技术", 
            "hobbies": ["旅行", "音乐"] 
        }
	]
}
```



### 论坛内容

> API端点：http://23.184.88.52:8000/api/posts/

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

## 发送帖子

请求头：

- **Authorization**: `Bearer <your-authentication-token>`
- **Content-Type**: `application/json`

请求体：

```json
{
    "user_id": "用户的唯一标识符",
    "method": "add",
    "post_title": "帖子的标题",
    "post_content": "帖子的内容",
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
    "method": "comment",
    "post_id": "每篇帖子的唯一编号",
    "comment_content": "评论的内容",
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



