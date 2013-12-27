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
        info: "login successful"
        identity: 'admin',
	}

    {
        info: "login successful"
        identity: 'worker',
	}

    {
        info: "login successful"
        identity: 'resident',
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
        'old_password': '旧密码',
        'new_password': '新密码',
        'repeat_password': '新密码',
    }

### Result:

#### Success
	{
	    'error': False,
		'info': '密码更新成功''
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

	{
		'error': True,
		'info': '两次密码不一致'
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
        'selected_pleased':'满意度'（1,2,3,4,5）5个数字选一个(默认是0)
    }

### Result:

#### Success

    {'success': True, 'info': '反馈成功！'}

#### Error

    {'success': False, 'info': '反馈失败！'}



### 9. User complain deal(用户需要登录)

#### URL : /api/complain/deal/

#### Method : POST

    {
        'complains_id_string': '要处理的投诉id号',（多个投诉id 拼接成字符串以逗号隔开 "1,2,32,45"）
        'deal_person_id': '指派的处理人的id',
    }
### Result:

#### Success

         {'success': True, 'info': '授权成功！'}

#### Error

        {'success': False, 'info': u'请选择要处理的投诉'}



### 10. User complain complete(用户需要登录)

#### URL : /api/complain/complete/

#### Method : POST

    {
        'complains_id_string': '要处理的投诉id号',（多个投诉id 拼接成字符串以逗号隔开 "1,2,32,45"）

    }
### Result:

#### Success

         {'success': True, 'info': '提交成功！'}




### 11. User own complain(用户需要登录)

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
                            deal_status: 1 (1,2,3  1代表未处理，2代表处理中...，3代表处理完成)
                            time: "2013-12-09 05:01:59+00:00"
                            type: "安全投诉"
                            id: 23
                            complain_author: "cainiao"
                            pleased: 0
                        }

                        {
                            content: "123F"
                            src: "uploads/2013/12/09/2_21.jpg"
                            deal_status: 1 (1,2,3  1代表未处理，2代表处理中...，3代表处理完成)
                            time: "2013-12-09 05:01:04+00:00"
                            type: "安全投诉"
                            id: 24
                            complain_author: "cainiao"
                            pleased: 0
                        }
                success:true
                ]
        }
#### Error

    {'success':false}


### 12. Get all complains list(用户需要登录)

#### URL :/api/show/all_complains/?page=页数&community_id=(小区id号)

#### Method : GET

#### Success
        {
           complains_list:
                [

                        {
                            content: "投诉内容"
                            src: "uploads/2013/12/26/a044ad345982b2b7a1f9f0cd33adcbef76099b51.jpg"
                            handler: "None"
                            deal_status: 1
                            time: "2013-12-26 01:50:06.514000+00:00"
                            type: "环境投诉"
                            id: 34
                            complain_author: "user2"
                            pleased: 0
                        }

                        {
                           content: "撒打算"
                            src: ""
                            handler: "worker1"
                            deal_status: 2
                            time: "2013-12-26 01:41:49.604000+00:00"
                            type: "安全投诉"
                            id: 33
                            complain_author: "sfi1234"
                            pleased: 0
                        }

                ]
             page_count: 1 页数
             success: true
        }


#### Error

        {'success': False}



### 13. User repair create(用户需要登录)

#### URL : /api/repair/create/

#### Method : POST
Content-Type: multipart/form-data;
category 和 category_item_id 必填

    {
        'content': '投诉内容',
        'category': '报修项目类型',（个人报修，公共报修） 二选一
        'category_item_id': '报修项目id号',
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



### 14. User repair response(用户需要登录)

#### URL : /api/repair/response/

#### Method : POST

    {
        'repair_id': '投诉id号',
        'response_content': '反馈内容',
        'selected_pleased':'满意度'（1,2,3,4,5）5个数字选一个(默认是0)
    }

### Result:

#### Success

    {'success': True, 'info': '反馈成功！'}

#### Error

    {'success': False, 'info': '反馈失败！'}


### 15. User own repair(用户需要登录)

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
                            deal_status: 1(1,2,3  1代表未处理，2代表处理中...，3代表处理完成)
                            time: "2013-12-05 06:02:18+00:00"
                            type: "弱电"
                            id: 3
                            repair_author: "菜菜"
                            pleased: 1
                        }

                        {
                            content: "十大发生的"
                            src: "uploads/2013/12/05/qq.jpg"
                            deal_status: 1 (1,2,3  1代表未处理，2代表处理中...，3代表处理完成)
                            time: "2013-12-05 05:01:17+00:00"
                            type: "电梯"
                            id: 1
                            repair_author: "菜菜"
                            pleased: 3
                        }
                success:true
                ]
        }
#### Error

    {'success':false}



### 16. User repair deal(用户需要登录)

#### URL : /api/repair/deal/

#### Method : POST

    {
        'repair_id_string': '要处理的报修id号',（多个投诉id 拼接成字符串以逗号隔开 "1,2,32,45"）
        'deal_person_id': '指派的处理人的id',
    }
### Result:

#### Success

         {'success': True, 'info': '授权成功！'}

#### Error

        {'success': False, 'info': u'请选择要处理的报修'}



### 17. User repair complete(用户需要登录)

#### URL : /api/repair/complete/

#### Method : POST

    {
        'repair_id_string': '要处理的投诉id号',（多个投诉id 拼接成字符串以逗号隔开 "1,2,32,45"）

    }
### Result:

#### Success

         {'success': True, 'info': '提交成功！'}





### 18. User own express(用户需要登录)

#### URL : /api/get/user/express/?page=页数 (page 可选, 默认为1)

#### Method : GET

### Result:

#### Success（每页返回20条记录）
        {
            page_count:（总页数）
            express_list:
                [

                        {
                            arrive_time: "2013-12-16 01:09:36+00:00"（快件到达时间）
                            deal_status: false (false:未领取，true:领取)
                            pleased: 0
                            express_author: "user3"
                            get_time: "None"（快件领取时间）
                            get_express_type: ""
                            id: 13
                        }


                ]
        }
#### Error

   {'success': False, 'info': '没有快递！'}


### 19. Get all express(用户需要登录)

#### URL : /api/show/all_express/?page=页数&community_id=小区id号 (page 可选, 默认为1)

#### Method : GET

### Result:

#### Success（每页返回20条记录）
        {
            page_count:（总页数）
            express_list:
                [

                        {
                            arrive_time: "2013-12-16 01:09:36+00:00"（快件到达时间）
                            deal_status: false (false:未领取，true:领取)
                            pleased: 0
                            express_author: "user3"
                            get_time: "None"（快件领取时间）
                            get_express_type: ""
                            id: 13
                        }

                success: true
                ]
        }
#### Error

   {'success': False, 'info': '没有快递！'}



### 20. User express response(用户需要登录)

#### URL : /api/express/response/

#### Method : POST

    {
        'express_id': '快递id号',
        'response_content': '反馈内容',
        'selected_pleased':'满意度'（1,2,3,4,5）5个数字选一个(默认是0)
    }

### Result:

#### Success

    {'success': True, 'info': '反馈成功！'}

#### Error

    {'success': False, 'info': '反馈失败！'}



### 21. User obtain express(用户需要登录)

#### URL : /api/user/obtain/express/

#### Method : POST

        {
            'express_id': '快递id号',
            'express_type': '取件方式',
            'allowable_get_express_time':'取件时间',
        }

#### Success

        {'success': True, 'info': '提交成功！'}



### 22. Find inhabitant(用户需要登录)

#### URL : /api/find/inhabitant/

#### Method : POST

        {
            'community_id': '小区的id',
            'building_num': '楼栋号',
            'room_num':'房间号',
        }

#### Success

        {'success': True, 'community_name': '香格里拉', 'building_num': 14, 'room_num': 101}

#### Error

        {'success': False, 'info': '没有此用户！'}


### 23. Delete express(用户需要登录)

#### URL : /api/express/delete/

#### Method : POST

         {
                'express_id_string': '要删除的快件id号',（多个快件id 拼接成字符串以逗号隔开 "1,2,32,45"）
         }

#### Success

        {'success': True, 'info': '删除成功！'}


### 24. Add express record(用户需要登录)

#### URL : /api/add/express/record/

#### Method : POST

        #### Method : POST

        {
            'community_id': '小区的id',
            'building_num': '楼栋号',
            'room_num':'房间号',
        }

#### Success

        {'success': True, 'info': '添加成功！'}

#### Error

        {'success': False, 'info': '添加失败！'}


### 25. Get communities(用户需要登录)

#### URL : /api/get/community/

#### Method : GET

#### Success

        {
            success:true
            community_list:
                [
                     {
                        community_description: "adfasdf"
                        id: 1
                        community_title: "sdfasdfasdf"
                     }
                ],

                [
                     {
                      community_description: "就是个小区"
                       id: 2
                       community_title: "香格里拉"
                     }
                ],

                [
                     {
                        community_description: "赖长青"
                        id: 3
                        community_title: "红楼"
                     }
                ]
            }
        }
#### Error

    {'success':false}


### 26. Express complete(用户需要登录)

#### URL : /api/express/complete/

#### Method :  POST

         {
                'express_id_string': '完成的快件id号',（多个快件id 拼接成字符串以逗号隔开 "1,2,32,45"）
         }

#### Success

        {'success': True, 'info': '完成领取！'}



### 27. Get repair item(用户需要登录)

#### URL : /api/get/repair/item/

#### Method :  GET

#### Success（每页返回五条记录）
        {
            page_count:（总页数）
            items_list:
                [

                        {
                            item_id: 2
                            item_type: "个人报修"
                            item_price: 123
                            item_name: "空调2"
                        }

                        {
                            item_id: 3
                            item_type: "公共报修"
                            item_price: 10000
                            item_name: "亭子"
                        }

                ]
             success: true
        }

#### Error

       {'success': False, 'info':'没有报修项目'}


### 28. Add repair item record(用户需要登录)

#### URL : /api/add/repair/item/record/

#### Method : POST


        {
            'item_type': '报修类型（个人报修，公共报修）',
            'item_name': '项目名称',
            'repair_item_price':'价格',
        }

#### Success

        {'success': True}

#### Error

        {'success': False}


### 29. Delete repair item(用户需要登录)

#### URL : /api/repair/item/delete/

#### Method : POST

         {
                'repair_item_id_string': '要删除报修项目id号',（多个id 拼接成字符串以逗号隔开 "1,2,32,45"）
         }

#### Success

        {'success': True, 'info': '删除成功！'}

#### Error

        {'success': False, 'info': '删除失败！'}



### 30. Get all repair list(用户需要登录)

#### URL :/api/show/all_repair/?page=页数community_id=小区id号

#### Method : GET

#### Success
        {
           repair_list:
                [

                        {
                            content: "阿萨德"
                            src: ""
                            handler: "None"
                            deal_status: 1
                            time: "2013-12-25 05:37:57.746000+00:00"
                            type: "个人报修"
                            id: 41
                            repair_author: "sfi123"
                            pleased: 0
                        }

                        {
                            content: "dfasd"
                            src: "uploads/2013/12/25/a044ad345982b2b7a1f9f0cd33adcbef76099b51.jpg"
                            handler: "worker1"
                            deal_status: 2
                            time: "2013-12-25 01:49:10.760000+00:00"
                            type: "个人报修"
                            id: 38
                            repair_author: "user3"
                            pleased: 0
                        }

                ]
             success: true
        }


#### Error

        {'success': False}

### 31. Get worker list(用户需要登录)

#### URL : /api/get/worker/list/?community_id=(小区id号)

#### Method : GET

#### Success

         {
            worker_list:
                [

                        {
                           username: "worker"
                           phone_number: "15862396507"
                           id: 4
                        }

                        {
                            username: "worker1"
                            phone_number: "15862396507"
                            id: 5
                        }

                ]
             success: true
             page_count:（总页数）
        }


#### Error

        {'success': False}



### 32. Modify repair item(用户需要登录)

#### URL : /api/api/modify/repair_item/

#### Method : POST（四个参数可以任意给一个）

     {
            'modify_item_id': '报修项目id',
            'item_type': '项目类型',（个人报修，公共报修）
            'item_name':'项目名称',
            'repair_item_price':'价格（必须为数字）',
     }

#### Success

         {'success': True}

#### Error

        {'success': False}


### 33 User submit housekeeping(用户需要登录)

#### URL : /api/user/submit_housekeeping/

#### Method : POST

     {
            'housekeeping_item_string': '家政项目id（多个项目 以字符串形式发送 如： 1,3,4）',

     }

#### Success

         {'success': True, 'info': '提交成功！'}


### 34 User submit response(用户需要登录)

#### URL : /api/housekeeping/response/

#### Method : POST

     {
            'housekeeping_id': '家政项目id',
            'response_content': 内容',
            'selected_pleased': '满意度（ 1,2,3,4,5）',

     }

#### Success

         {'success': True, 'info': '反馈成功！'}


#### Error

        {'success': False, 'info': '反馈失败！'}


### 35 User get own housekeeping(用户需要登录)

#### URL : /api/own/housekeeping/

#### Method : GET

#### Success

         {
            house_keep_list:
                [

                        {
                            content: "一般性家庭保洁"
                            housekeeping_status: 2
                            handler: "worker9"
                            item: "钟点工"
                            remarks: "小于20小时每月，两小时起步。"
                            price_description: "40元/小时"
                            time: "2013-12-25 08:54:32.425000+00:00"
                            id: 8
                            housekeeping_author: "sfi12345"
                            pleased: 0
                        }

                        {
                            content: "一般性家庭保洁"
                            housekeeping_status: 2
                            handler: "worker9"
                            item: "钟点工"
                            remarks: "小于20小时每月，两小时起步。"
                            price_description: "40元/小时"
                            time: "2013-12-25 08:32:11.428000+00:00"
                            id: 7
                            housekeeping_author: "user3"
                            pleased: 0
                        }

                ]
             success: true
             page_count:（总页数）
        }

#### Error

        {'success': False}


### 36 Deal housekeeping(用户需要登录)

#### URL : /api/housekeeping/deal/

#### Method : POST

     {
            'housekeeping_id_string': ''家政项目id（多个项目 以字符串形式发送 如： 1,3,4）'
            'deal_person_id': 处理人id',

     }

#### Success

         {'success': True, 'info': u'授权成功！'}


#### Error

        {'success': False}


### 37 Housekeeping complete(用户需要登录)

#### URL : /api/housekeeping/complete/

#### Method : POST

     {
            'housekeeping_id_string': ''家政项目id（多个项目 以字符串形式发送 如： 1,3,4）'

     }

#### Success

        {'success': True, 'info': '提交成功！'}



### 38 Show all housekeeping(用户需要登录)

#### URL : /api/show/all_housekeeping/?community_id=小区id&page=页数

#### Method : GET

#### Success

         {
            house_keep_list:
                [

                        {
                            content: "一般性家庭保洁"
                            housekeeping_status: 2
                            handler: "worker9"
                            item: "钟点工"
                            remarks: "小于20小时每月，两小时起步。"
                            price_description: "40元/小时"
                            time: "2013-12-25 08:54:32.425000+00:00"
                            id: 8
                            housekeeping_author: "sfi12345"
                            pleased: 0
                        }

                        {
                            content: "一般性家庭保洁"
                            housekeeping_status: 2
                            handler: "worker9"
                            item: "钟点工"
                            remarks: "小于20小时每月，两小时起步。"
                            price_description: "40元/小时"
                            time: "2013-12-25 08:32:11.428000+00:00"
                            id: 7
                            housekeeping_author: "user3"
                            pleased: 0
                        }

                ]
             success: true
             page_count:（总页数）
        }

#### Error

        {'success': False}


### 39. Get housekeeping item(用户需要登录)

#### URL : /api/get/housekeeping_item/

#### Method :  GET

#### Success（每页返回五条记录）
        {
            page_count:（总页数）
            items_list:
                [

                        {
                            item_id: 3
                            item_detail.remarks: "大于20小时每月，两小时起步。"
                            item_content: "一般性家庭保洁"
                            price_description: "30元/小时"
                            item_name: "钟点工"
                        }

                        {
                            item_id: 4
                            item_remarks: "小于20小时每月，两小时起步。"
                            item_content: "一般性家庭保洁"
                            price_description: "40元/小时"
                            item_name: "钟点工"
                        }

                ]
             success: true
        }

#### Error

       {'success': False, 'info':'没有家政项目'}


### 40. Add housekeeping item (用户需要登录)

#### URL : /api/add/housekeeping_item/

#### Method : POST


        {
            'housekeeping_price_description': '价格描述',
            'housekeeping_item_name': '项目名称',
            'housekeeping_content':'内容',
            'housekeeping_remarks':'备注',
        }

#### Success

        {'success': True}

#### Error

        {'success': False}


### 41. Delete housekeeping item(用户需要登录)

#### URL : /api/delete/housekeeping_item/

#### Method : POST

         {
                'selected_item_string': '要删除家政项目id号',（多个id 拼接成字符串以逗号隔开 "1,2,32,45"）
         }

#### Success

        {'success': True, 'info': '删除成功！'}

#### Error

        {'success': False, 'info': '删除失败！'}


### 42. Modify housekeeping item(用户需要登录)

#### URL : /api/modify/housekeeping_item/

#### Method : POST（四个参数可以任意给一个）

     {
            'modify_item_id': '家政项目id',
            'modify_price_description': 价格描述',
            'modify_item_name': '项目名称'
            'modify_content':'内容',
            'modify_remarks':'备注',
     }

#### Success

         {'success': True}

#### Error

        {'success': False}
