#coding:utf-8
 #!/usr/bin/env python

# @Time    : 2016/11/7 10:34
# @Author  : eric
# @Site    : 
# @File    : upxlwt.py
# @Software: PyCharm

from django.http import HttpResponse,HttpResponseRedirect
from xlwt import *
from assets.models import Dept
from django.contrib.auth.decorators import login_required
import os,re
import StringIO
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "www.settings")
import django

django.setup()
import xlrd
import tkFileDialog

from assets.forms import UpdeptForm
from superauto import settings
from time import strftime,localtime
from xlrd import open_workbook,cellname
import traceback
from django.shortcuts import render_to_response
from django.template import RequestContext


@login_required
def deptup(request):
    username=request.user.username
    if request.POST:
        form=UpdeptForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                xlsfiles=request.FILES.get('deptform','')
                filename=xlsfiles.name
                #创建文件存储路径
                fname = os.path.join(settings.MEDIA_ROOT, 'uploads/dept/%s' % strftime("%Y/%m/%d", localtime()),
                                     filename)
                if os.path.exists(fname):
                    os.remove(fname)
                dirs = os.path.dirname(fname)
                if not os.path.exists(dirs):
                    os.makedirs(dirs)
                #写入文件
                if os.path.isfile(fname):
                    os.remove(fname)
                content=xlsfiles.read()
                fp=open(fname,'wb')
                fp.write(content)
                fp.close()


                #格式化数据保存到数据库
                book = xlrd.open_workbook(fname)
                sheet = book.sheet_by_index(0)  # 获取工作表
                for row_index in range(1,sheet.nrows):
                    record = sheet.row_values(row_index, 0)
                    try:
                        pd=record[2].strip()
                        if pd:
                            parentid = Dept.objects.get(deptname=pd)
                            dept = Dept(deptname=str(record[1].rstrip(".0")), parentdept=parentid)
                        else:
                            dept = Dept(deptname=str(record[1]).rstrip(".0"))
                        dept.save()
                    except Dept.DoesNotExist, e:
                        traceback.print_stack()
                        traceback.print_exc()
                        print e
                successinfo = "上传"
                success = True
                return render_to_response('include/dept/updept.html', {
                    "title": '导入部门',
                    'form': form,
                    'successinfo': successinfo,
                    'success': success,
                    'username': username}, context_instance=RequestContext(request))
            except Exception, e:
                traceback.print_stack()
                traceback.print_exc()
                print e
        else:
            return render_to_response('include/dept/updept.html', {
                "title": '导入部门',
                'form': form,
                'username': username}, context_instance=RequestContext(request))
    #return render_to_response('include/dept/updept.html', {
               # "title": '导入部门',
              #  'username': username}, context_instance=RequestContext(request))


    return render_to_response('include/dept/updept.html', RequestContext(request))



@login_required
def dept_xlrd(request):

    xlsfile = r'D:\xls\cs.xls'
    data = xlrd.open_workbook(xlsfile)
    table = data.sheet_by_index(0)  # 获取工作表
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(0)
    WorkList = []
    x = y = z = 0
    hav_list=Dept.objects.all()
    for i in range(1, nrows):
        row = table.row_values(i)
        y = y + 1
        for j in range(0, ncols):
            if type(row[j]) == float:  # 如果值为float则转换为int,避免出现1输出为1.0的情况
                row[j] = int(row[j])
        if row:
            y=y+1

            WorkList.append(
                    Dept(id=row[0], deptname=row[1], parentdept_id=None)
                    )


    try:
        Dept.objects.bulk_create(WorkList)


    except:
        return HttpResponse('数据格式错误:请检查ID是否与数据库重复')
    return HttpResponse('导入数据成功')


@login_required
def dept_xlwt(request):
    list_obj=Dept.objects.all().order_by('id')
    style_heading = easyxf("""
            font:
                name SimSun,
                colour_index black,
                bold on,
                height 300;
            align:
                wrap off,
                vert center,
                horiz center;

            pattern:
                pattern solid,
                fore-colour 0x19;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
                """
                           )
    style_body = easyxf("""
            font:
                name Arial,
                bold off,
                height 250;
            align:
                wrap on,
                vert center,
                horiz left;
            borders:
                left THIN,
                right THIN,
                top THIN,
                bottom THIN;
            """
                             )
    style_green = easyxf(" pattern: pattern solid,fore-colour 0x11;")
    style_red = easyxf(" pattern: pattern solid,fore-colour 0x0A;")
    fmts = [
        'M/D/YY',
        'D-MMM-YY',
        'D-MMM',
        'MMM-YY',
        'h:mm AM/PM',
        'h:mm:ss AM/PM',
        'h:mm',
        'h:mm:ss',
        'M/D/YY h:mm',
        'mm:ss',
        '[h]:mm:ss',
        'mm:ss.0',
    ]


    if list_obj:

        ws=Workbook(encoding = 'utf-8')

        sheet=ws.add_sheet(u'部门表',cell_overwrite_ok=True)
        first_col = sheet.col(0)  # xlwt中是行和列都是从0开始计算的
        sec_col = sheet.col(1)
        thr_col=sheet.col(2)

        first_col.width = 256 * 20
        sec_col.width = 256 * 20
        thr_col.width = 256 * 20
        sheet.write(0, 0, u"id",style_heading)
        sheet.write(0, 1, u"部门",style_heading)
        sheet.write(0, 2, u"上级部门",style_heading)

        #写入数据
        excel_row = 1
        for obj in list_obj:
            dept_id=obj.id
            dept_name=obj.deptname
            if not obj.parentdept:

                dept_parent=" "

            else:
                dept_parent=obj.parentdept.deptname


            sheet.write(excel_row, 0, str(dept_id),style_body)
            sheet.write(excel_row, 1, dept_name,style_body)
            sheet.write(excel_row, 2, dept_parent,style_body)
            excel_row += 1


        fname='deptfile.xls'
        agent=request.META.get('HTTP_USER_AGENT')

        output = StringIO.StringIO()
        ws.save(output)
        output.seek(0)
        response = HttpResponse(output.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s'%fname
        response.write(output.getvalue())
        return response



