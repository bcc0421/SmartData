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
		'info':u'仅限管理员访问'
	}

### 5. Logout

#### URL : /api/user/logout/

#### Method : POST

    {
    }

### Result:

#### Success
	{
		'info':u'成功登出'
	}
