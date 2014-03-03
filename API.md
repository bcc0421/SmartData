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



### 9. User complain deal(用户需要登录)（管理员调用）

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



### 10. User complain complete(用户需要登录)(工作人员调用)

#### URL : /api/complain/complete/

#### Method : POST

    {
        'complains_id_string': '要处理的投诉id号',（多个投诉id 拼接成字符串以逗号隔开 "1,2,32,45"）

    }
### Result:

#### Success

         {'success': True, 'info': '提交成功！'}




### 11. User own complain(用户需要登录)（此接口得到用户自己所有的数据 ，第39个根据处理状态进行了分类）

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


### 12. User repair create(用户需要登录)

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



### 13. User repair response(用户需要登录)

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


### 14. User own repair(用户需要登录)（此接口得到用户自己所有的数据 ，第40个根据处理状态进行了分类）

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



### 15. User repair deal(用户需要登录)（管理员调用）(报修由未受理变改为已受理)

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



### 16. User repair complete(用户需要登录)（工作人员调用）

#### URL : /api/repair/complete/

#### Method : POST

    {
        'repair_id_string': '要处理的投诉id号',（多个投诉id 拼接成字符串以逗号隔开 "1,2,32,45"）

    }
### Result:

#### Success

         {'success': True, 'info': '提交成功！'}





### 17. User own express(用户需要登录)（此接口得到用户自己所有的数据 ，第42个根据领取状态进行了分类）

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



### 18. User express response(用户需要登录)

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



### 19. User obtain express(用户需要登录)（用户调用 用户点击领取快件的时候调用）

#### URL : /api/user/obtain/express/

#### Method : POST

        {
            'express_id': '快递id号',
            'express_type': '取件方式',
            'allowable_get_express_time':'取件时间',
        }

#### Success

        {'success': True, 'info': '提交成功！'}



### 20. Find inhabitant(用户需要登录)（工作人员调用，增加快递是查询该用户是否存在）

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


### 21. Delete express(用户需要登录)

#### URL : /api/express/delete/

#### Method : POST

         {
                'express_id_string': '要删除的快件id号',（多个快件id 拼接成字符串以逗号隔开 "1,2,32,45"）
         }

#### Success

        {'success': True, 'info': '删除成功！'}


### 22. Add express record(用户需要登录)（工作人员调用）

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


### 23. Get communities(用户需要登录)

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


### 24. Express complete(用户需要登录)（工作人员或管理员调用在用户已将快件取走是 工作人员或管理员调用来更改状态）

#### URL : /api/express/complete/

#### Method :  POST

         {
                'express_id_string': '完成的快件id号',（多个快件id 拼接成字符串以逗号隔开 "1,2,32,45"）
         }

#### Success

        {'success': True, 'info': '完成领取！'}



### 25. Get repair item(用户需要登录)（管理员调用）

#### URL : /api/get/repair/item/?type=(个人，公共)二选一 不传参数返回所有

#### Method :  GET

#### Success（每页返回五条记录）
        {

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


### 26. Add repair item record(用户需要登录)（管理员调用）

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


### 27. Delete repair item(用户需要登录)（管理员调用）

#### URL : /api/repair/item/delete/

#### Method : POST

         {
                'repair_item_id_string': '要删除报修项目id号',（多个id 拼接成字符串以逗号隔开 "1,2,32,45"）
         }

#### Success

        {'success': True, 'info': '删除成功！'}

#### Error

        {'success': False, 'info': '删除失败！'}




### 28. Get worker list(用户需要登录)（管理员调用）

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



### 29. Modify repair item(用户需要登录)（管理员调用）

#### URL : /api/modify/repair_item/

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


### 30 User submit housekeeping(用户需要登录)（用户调用 提交家政项目）

#### URL : /api/user/submit_housekeeping/

#### Method : POST

     {
            'housekeeping_item_string': '家政项目id（多个项目 以字符串形式发送 如： 1,3,4）',

     }

#### Success

         {'success': True, 'info': '提交成功！'}


### 31 User submit response(用户需要登录)

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


### 32 User get own housekeeping(用户需要登录)（获得用户自己已提交的家政服务，第41根据处理状态进行了分类）

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


### 33 Deal housekeeping(用户需要登录)

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


### 34 Housekeeping complete(用户需要登录)（工作人员调用）

#### URL : /api/housekeeping/complete/

#### Method : POST

     {
            'housekeeping_id_string': ''家政项目id（多个项目 以字符串形式发送 如： 1,3,4）'

     }

#### Success

        {'success': True, 'info': '提交成功！'}



### 35. Get housekeeping item(用户需要登录)（管理员和用户调用，用户调用 显示所有服务项目 一边选择，管理员得到所有项目便于管理）

#### URL : /api/get/housekeeping_item/?page=页数

#### Method :  GET

#### Success（每页返回五条记录）
        {
            page_count:（总页数）
            items_list:
                [

                        {
                            item_id: 3
                            item_remarks: "大于20小时每月，两小时起步。"
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


### 36. Add housekeeping item (用户需要登录)（管理员调用）

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


### 37. Delete housekeeping item(用户需要登录)（管理员调用）

#### URL : /api/delete/housekeeping_item/

#### Method : POST

         {
                'selected_item_string': '要删除家政项目id号',（多个id 拼接成字符串以逗号隔开 "1,2,32,45"）
         }

#### Success

        {'success': True, 'info': '删除成功！'}

#### Error

        {'success': False, 'info': '删除失败！'}


### 38. Modify housekeeping item(用户需要登录)（管理员调用）

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

### 39. Get complains by status(用户需要登录)（工作人员 管理员 用户 调用此接口 得到各自对应的数据）

#### URL :/api/show/complains_by_status/?page=页数&community_id=(小区id号)&status=1(未受理)，2(处理中)，3(已处理),4(已受理)， 如果是工作人员 status=2(处理中)，3(已处理),4(已受理)3选一

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



### 40. Get repair by status(用户需要登录)（工作人员 管理员 用户 调用此接口 得到各自对应的数据）

#### URL :/api/show/repair_by_status/?page=页数&community_id=(小区id号)&status=1(未受理)，2(处理中)，3(已处理),4(已受理)， 如果是工作人员 status=2(处理中)，3(已处理),4(已受理)3选一


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


### 41 Show housekeeping by status(用户需要登录)（工作人员 管理员 用户 调用此接口 得到各自对应的数据）

#### URL : /api/show/housekeeping_by_status/?page=页数&community_id=(小区id号)&status=(未处理，处理中，已处理)三选一，如果是工作人员 status=(处理中，已处理)二选一

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




### 42. Get express by status(用户需要登录)（工作人员 管理员 用户 调用此接口 得到各自对应的数据，管理员可以看所有小区的 工作人员只可以看本小区的 不存在指派给功能）

#### URL : /api/show/express_by_status/?page=页数&community_id=(小区id号)&status=(领取，未领取)2选一

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



### 43. Get dynamic data number(用户需要登录)(消息提醒显示最新数据)（得到新增的数目）

#### URL : /api/get_dynamic_data_num/

#### Method : GET

### Result:

#### Success
        {

                repair_num: 7
                housekeeping_num: 0
                sum_num: 7
                complain_num: 0
                express_num: 0

        }


### 44. Get channel and user id(用户需要登录)(绑定手机短)

#### URL : /api/get_channel_user_id/

#### Method : POST

    {
            'channel_id': '频道id',
            'user_id': '手机用户id',
            'device_type':手机类型

     }

### Result:

#### Success

        {'success': True, 'info': u'绑定成功'}

#### Error

        {'success': False, 'info': '没有传入相关信息'}


### 45. Get dynamic data/(用户需要登录)(获取最新消息的详细内容)

#### URL : /api/get_dynamic_data/

#### Method : POST

    {
            'item_name': '(housekeeping, complain, express,repair)传入获取的类型 四选一',

     }

### Result:

#### Success

        {'complain_list': complain_list, 'success': True, 'identity': 'admin'}

#### Error

        { 'success': False}



### 46. 工作人员修改状态处理状态改成处理中（之前所调用的接口，已改成已受理的状态）

#### URL : /api_worker/deal/repair/

#### Method : POST

    {
            'repair_id_string': '要处理的报修id号',（多个投诉id 拼接成字符串以逗号隔开 "1,2,32,45"）,
     }

### Result:

#### Success

        response_data = {'success': True, 'info': ''}

#### Error

        { 'success': False}


### 47. 工作人员修改状态处理状态改成处理中（之前所调用的接口，已改成已受理的状态）

#### URL : /api_worker/deal/complain/

#### Method : POST

    {
            'complains_id_string': '要处理的投诉id号',（多个投诉id 拼接成字符串以逗号隔开 "1,2,32,45"）,
     }

### Result:

#### Success

        response_data = {'success': True, 'info': ''}

#### Error

        { 'success': False}