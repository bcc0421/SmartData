# Smart Data API

## User Admin

### 1. Create user

#### URL : /api/user/create/

#### Method : POST

    {
        'username': '用户名',
        'password': '密码',
        'repeatPwd': '密码',
        'mobile': '11位手机号码',
        'email': '电子邮箱',
		'community': '1', (小区的主键)
		'is_admin': '1', ('0':业主, '1':工作人员, '2':管理员)
		'floor': '楼栋号',
		'gate_card': '门牌号',
		'address': '详细地址'
    }

### Result:

#### Success
	{
		'info': 'create user successful'
	}

#### Error
	{
		'username_error': True, 
		'info': '用户名已存在'
	}

	{
		'password_error': True, 
		'info': '两次密码输入不相同'
	}

	{
		'password_error': True, 
		'info': '密码：字母、数字组成，6-15位'
	}

	{
		'mobile_error': True, 
		'info': '请输入正确的手机号码'
	}

	{
		'email_error': True, 
		'info': '请输入正确的邮箱地址
	}


### 2. Login

#### URL : /api/user/login/

#### Method : POST

    {
        'username': '用户名',
        'password': '密码'
    }

### Result:

#### Success
	{
		'info': 'login successful'
	}

#### Error
	{
		'info': 'login failed'
	}

### 3. Update user detail (用户需要登录)

#### URL : /api/user/update/

#### Method : POST

    {
        'username': '用户名',
        'mobile': '11位手机号码',
        'email': '电子邮箱',
		'community': '1', (小区的主键)
		'floor': '楼栋号',
		'gate_card': '门牌号',
		'address': '详细地址'
    }

### Result:

#### Success
	{
		'info': 'update profile detail successful'
	}

#### Error
	{
		'mobile_error': True, 
		'info': '请输入正确的手机号码'
	}

	{
		'email_error': True, 
		'info': '请输入正确的邮箱地址'
	}

### 4. Change password (用户需要登录)

#### URL : /api/user/change_password/

#### Method : POST

    {
		'username': '用户名'
        'old_password': '旧密码',
        'new_password': '新密码',
    }

### Result:

#### Success
	{
		'info': 'update profile detail successful'
	}

#### Error
	{
		'error': True, 
		'info': '密码长度为6-15位数字或字母'
	}

	{
		'error': True, 
		'info': '旧密码不正确'
	}

### 5. User list （需要管理员登录才能访问）

#### URL : /api/user/list/

#### Method : POST

    {
    }

### Result:

#### Success
	[
	  {
	    "username": "asdf",
	    "phone_number": "12345678901",
	    "floor": null,
	    "address": null,
	    "gate_card": null,
	    "id": 4,
	    "community": "别院",
	    "email": ""
	  },
	  {
	    "username": "fanjie",
	    "phone_number": "12345678901",
	    "floor": null,
	    "address": null,
	    "gate_card": null,
	    "id": 5,
	    "community": "别院",
	    "email": ""
	  },
	  {
	    "username": "robiner",
	    "phone_number": "12345678901",
	    "floor": null,
	    "address": null,
	    "gate_card": null,
	    "id": 3,
	    "community": "别院",
	    "email": ""
	  }
	]

#### Error
	{
		'error':True,
		'info':'仅限管理员访问'
	}

### 6. Logout

#### URL : /api/user/logout/

#### Method : POST

    {
    }

### Result:

#### Success
	{
		'info':'成功登出'
	}


### 7. User complain create(用户需要登录)

#### URL : /api/complain/create/

#### Method : POST
Content-Type: multipart/form-data;
content 和category (必须有一个给值)

    {
        'content': '投诉内容',
        'category': '投诉类型',    目前为（安全投诉，环境投诉，员工投诉）中三选一
        'upload_complain_img':'filename'
    }

### Result:

#### Success
    {
        'error': False,
        'info': u'投诉创建成功'
    }

#### Error
    {
        'error': True,
        'info': u'投诉创建失败'

    }

### 8. User complain response(用户需要登录)

#### URL : /api/complain/response/

#### Method : POST

    {
        'complain_id': '投诉id号',
        'response_content': '反馈内容',
        'selected_pleased':'满意度'（1,2,3,4,5）5个数字选一个
    }

### Result:

#### Success

    {'success': True, 'info': '反馈成功！'}

#### Error

    {'success': False, 'info': '反馈失败！'}


### 9. User own complain(用户需要登录)

#### URL : /api/own/complain/?page=页数 (page 可选, 默认为1)

#### Method : GET

### Result:

#### Success（每页返回五条记录）
        {
            page_count:（总页数）
            complain_list:
                [

                        {
                            content: "sgsdfgsdfgdfsgsdf"
                            src: "uploads/2013/12/09/2_18.jpg"
                            deal_status: false
                            time: "2013-12-09 05:01:59+00:00"
                            type: "安全投诉"
                            id: 23
                            complain_author: "cainiao"
                            pleased: 0
                        }

                        {
                            content: "123F"
                            src: "uploads/2013/12/09/2_21.jpg"
                            deal_status: false
                            time: "2013-12-09 05:01:04+00:00"
                            type: "安全投诉"
                            id: 24
                            complain_author: "cainiao"
                            pleased: 0
                        }

                ]
        }

### 10. User repair create(用户需要登录)

#### URL : /api/repair/create/

#### Method : POST
Content-Type: multipart/form-data;
content 和category (必须有一个给值)

    {
        'content': '投诉内容',
        'category': '投诉类型',    目前为（安全投诉，环境投诉，员工投诉）中三选一
        'upload_repair_img':'filename'
    }

### Result:

#### Success
    {
        'error': False,
        'info': u'报修创建成功'
    }

#### Error
    {
        'error': True,
        'info': u'报修创建失败'

    }

### 11. User repair response(用户需要登录)

#### URL : /api/repair/response/

#### Method : POST

    {
        'repair_id': '投诉id号',
        'response_content': '反馈内容',
        'selected_pleased':'满意度'（1,2,3,4,5）5个数字选一个
    }

### Result:

#### Success

    {'success': True, 'info': '反馈成功！'}

#### Error

    {'success': False, 'info': '反馈失败！'}


### 12. User own repair(用户需要登录)

#### URL : /api/own/repair/?page=页数 (page 可选, 默认为1)

#### Method : GET

### Result:

#### Success（每页返回五条记录）
        {
            page_count:（总页数）
            repair_list:
                [

                        {
                            content: "123"
                            src: ""
                            deal_status: true
                            time: "2013-12-05 06:02:18+00:00"
                            type: "弱电"
                            id: 3
                            repair_author: "菜菜"
                            pleased: 1
                        }

                        {
                            content: "十大发生的"
                            src: "uploads/2013/12/05/qq.jpg"
                            deal_status: true
                            time: "2013-12-05 05:01:17+00:00"
                            type: "电梯"
                            id: 1
                            repair_author: "菜菜"
                            pleased: 3
                        }

                ]
        }
