#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2016/11/2 16:46
# @Author  : eric
# @Site    : 
# @File    : validators.py
# @Software: PyCharm

import re
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

username_re = re.compile(r'^([\w]{9}|[a-zA-Z]{1}[\w]+?)$')
username = RegexValidator(username_re,u'管理员:6-12位,由字母数字下划线组成,首字母为字母','invalid')

password_re = re.compile(r'^[\w]+?$')
password = RegexValidator(password_re,u'密码由字母数字下划线组成的字符串，最少为6位','invalid')

classid_re = re.compile(r'^[\w]{7}$')
classid = RegexValidator(classid_re,u'班号由7位数数字组成','invalid')

classname_re = re.compile(r'^[\u4e00-\u9fa5]{2,6}$')
