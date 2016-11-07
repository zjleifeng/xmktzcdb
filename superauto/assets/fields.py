#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/2 16:43
# @Author  : eric
# @Site    : 
# @File    : fields.py
# @Software: PyCharm
from django.forms.fields import CharField
from validators import username,password

class UsernameField(CharField):
    default_error_messages = {
        'invalid': u'管理员:6-12位,由字母数字下划线组成,首字母为字母',
        'required': u'用户名必须要填(管理员:6-12位,由字母数字下划线组成,首字母为字母)',
        'max_length': u'管理员用户名至多为12位',
        'min_length': u'管理员用户名至少为6位'
    }

    default_validators = [username]

    def clean(self, value):
        value=self.to_python(value).split()
        return super(UsernameField,self).clean(value)

class PasswordField(CharField):
    default_error_messages = {
        'invalid': u'密码由字母数字下划线组成的字符串，最少为8位',
        'required': u'密码必须要填(由字母数字下划线组成的字符串，最少为6位)',
        'max_length': u'密码至多为16位',
        'min_length': u'密码至少为8位'
    }
    default_validators = [password]