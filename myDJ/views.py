from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
import psycopg2
conn = psycopg2.connect(database="contract", user="postgres", password="88888", host="10.60.120.31", port="5432")
cursor= conn.cursor()
import openpyxl as op

def register(request):
    return render(request, "register.html")



def login(request):
    return render(request, "login.html")

def dowload(request):
    return render(request,"dowload.html")


def dowload1(request):
    data = []
    # for i in range(3):
    # a1=request.POST.get('data1')
    a1 = request.POST.getlist('data1')
    for a in a1:

        print("a为",a)
        cursor.execute(
            """SELECT * from check_information inner join commodity_information on check_information.id1=commodity_information.product_id where pre_recorded= %s""",
            [a])
        data1 = cursor.fetchall()
        data.append(data1)


    # for a in a1:
    #     print("每条记录为",a)
    # cursor.execute(
    #     """SELECT * from check_information inner join commodity_information on check_information.id1=commodity_information.product_id where pre_recorded= %s""",
    #     [a])
    # data1 = cursor.fetchall()
    # data.append(data1)
    # b = request.POST.get('data2')
    # c = request.POST.get('data3')
    # a=request.getParameterValues('data1')
    # print("a,b,c",a)
    wb=op.Workbook()
    # cursor.execute("""SELECT * from check_information inner join commodity_information on check_information.id1=commodity_information.product_id where pre_recorded= %s""", [a1])
    # data=cursor.fetchall()
    ws=wb["Sheet"]
    title=['预录入统一编号','清单编号','手(账)册编号','经营企业编码','经营企业社会信用代码','经营企业名称','申报单位代码','申报单位社会信用代码',
           '申报单位名称','企业内部编号','录入日期','清单申报日期','料件、成品标志','监管方式','运输方式','进出境关别','主管海关','核扣标志','录入单位代码','录入单位社会信用代码',
           '录入单位名称','报关标志','报关类型','报关单类型','对应报关单编号','对应报关单申报单位代码','对应报关单申报单位名称','对应报关单申报单位社会信用代码','清单类型','关联清单编号',
           '关联手(账)册备案号','报关单申报日期','备注','清单进出卡口状态','申请表编号','流转类型','关联报关单编号','关联报关单境内收发货人代码','收发货人名称','社会信用代码','关联报关单生产销售(消费使用)单位代码',
           '单位名称','关联报关单申报单位代码','申报单位名称','类别','id','商品序号','备案序号','商品料号','商品编码','商品名称','规格型号','产销国（地区）','申报单价','申报总价',
           '币制','申报数量','申报单位','法定单位','法定数量','法定第二单位','法定第二数量','征免方式','单耗版本号','商品ID','类别']
    print("标题",title)
    print("值",data)
    ws.append(title)
    for i in range(len(data)):
        for j in range(len(data[i])):
            print("j为",i)
            # for j in i:
            d=data[i][j]
            print("d为",d)
            ws.append(d)
    wb.save("re1.xlsx")
    #
    # return render(request,"down.html")
    excel = open('re1.xlsx', "rb")
    # FileResponse 该类可以将文件下载到浏览器
    response = FileResponse(excel)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('file_name.xlsx')
    return response



def dowload2(request):
    a =request.POST.get('data1')
    # b = request.POST.get('data2')
    # c = request.POST.get('data3')
    print("abc为",a)
    return HttpResponse({"msg":"导出成功","code":200})


def login1(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    print("登录姓名为:", username)
    cur = conn.cursor()
    cur.execute("""SELECT * FROM user1 where username1 = %s and passd1 = %s""", (username, password))
    a = cur.fetchall()
    print("登录信息为:", a)
    if len(a) == 1:
        return show(request)
    if len(a) == 0:
        messages.error(request, "输入错误！，请重新输入")
        return render(request, "login.html")


def register1(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM user1 where username1 = %s and passd1 = %s """, (username, password))

    a = cur.fetchall()
    print(len(a))
    print(a)
    if len(a) == 1:
        messages.error(request, "该用户已注册，请重新输入")
        return render(request, "register.html")

    else:
        cur.execute("""insert into user1(username1,passd1) values(%s, %s)""",
                    (username, password))
        conn.commit()
        messages.error(request, "注册成功！")
        return render(request, "login.html")





def p_data(request):
    if request.method == 'GET':
        username = request.GET.get("username")
        # username = request.POST.get('username')
        print("hi在", username)
        conn = psycopg2.connect(database="contract", user="postgres", password="88888", host="10.60.120.31", port="5432")
        cursor = conn.cursor()
        # cur = conn.cursor()
        cursor.execute("""SELECT  pre_recorded,listing_number,book_number,enterprise_code,credit_code,enterprise_name
     ,applicant_code,applicant_credit_code,applicant_Name,enterprise_internal_number,entry_date,list_declaration_date,
      products_marks,regulatory,transportation,entry_exit,customs,nuclear_button,input_code,input_social_credit_code,
      input_social_credit_name,customs_mark,list_type,customs_declaration_date,note FROM check_information where pre_recorded = %s""", [username])
        a = cursor.fetchall()
        data=[]
        for i in a:
            for j in i:
                data.append(j)
        #     print("每个值为",i)
        # print("获取到的值为", a)
        # # print("第一个值",data[0])
        # cursor.execute("""SELECT * FROM  user where username = %s""", [username])
        cursor.execute("""SELECT product_serial_number, record_serial_number,commodity_materials_issue,commodity_code,commodity_name,specifications,pin_countries,declare_unit_price,declare_total_price,monetary,declaration_quantity,notification,legal_units,legal_number,statutory_second_unit,statutory_second_quantity,a_new_way,single_consumption_version from
         commodity_information right join check_information on commodity_information.product_id = check_information.id1 where check_information.pre_recorded = %s""", [username])
        a1=cursor.fetchall()
        data1=[]
        for i1 in a1:
            for j1 in i1:
                data1.append(j1)

        # print("===", a1)
        # print("data1",data1)
        # shang(username)
        return render(request, 't.html', {'data': data,'a1':a1})


def search_by_word(request):
    username = request.POST.get('word')
    username1='%'+username+'%'
    print("搜索编号",username1)
    cursor.execute("""SELECT  * FROM check_information where pre_recorded like %s """, [username1])
    a = cursor.fetchall()
    print("查询信息为:",a)

    str2 = ""
    str3 = ""
    if len(a) == 0:
        # messages.error(request, "没有该清单编号")
        return render(request,"mess.html")
        # return show(request)
        # cursor.execute("""SELECT pre_recorded,listing_number,book_number,enterprise_code,credit_code,enterprise_name
        #      ,applicant_code,applicant_credit_code,applicant_Name,enterprise_internal_number,entry_date,list_declaration_date,
        #       products_marks,regulatory,transportation,entry_exit,customs,nuclear_button,input_code,input_social_credit_code,
        #       input_social_credit_name,customs_mark,list_type,customs_declaration_date,note FROM  check_information  """)
        # a = cursor.fetchall()
        # # print("信息",a)
        #
        # # for i in a:
        # #     print("编号",i)
        #
        # return render(request, 'show.html', {'a': a})
    else:
        return render(request, "show.html", {'a': a})



from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
def show(request):
    # conn = MySQLdb.connect(host="localhost", user="root", passwd="123456", db="test", charset="utf8")
    # with conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) as cursor:
        # cur = conn.cursor()
    # curr_page = request.GET["page"]
    # a=int (curr_page)* 3
    # sql = "SELECT *, (select count (*) from check_information) from check_information limit " + str(a) + "3;"
    # cursor.execute(sql)
    # info = cursor.fetchal1()
    # results = []
    # for i in info:
    #     results.append({'id': i[0], "95月xn头ms ": i[1]})
    #     count = i[2]
    # if count%3==0:
    #     num_pages=count/3
    # else:
    #     num_pages = count/3+1
    # last_pages = int(num_pages)-1
    # int_curr_page = int(curr_page)
    # if int_curr_page == 0:
    #     has_previous = False
    # else:
    #     has_previous = True
    # if int_curr_page == int(num_pages) - 1:
    #     has_next = False
    # else:
    #     has_next = True
    # previous_page_number = int_curr_page - 1
    # next_page_number = int_curr_page + 1

    cursor.execute("""SELECT pre_recorded,listing_number,book_number,enterprise_code,credit_code,enterprise_name
     ,applicant_code,applicant_credit_code,applicant_Name,enterprise_internal_number,entry_date,list_declaration_date,
      products_marks,regulatory,transportation,entry_exit,customs,nuclear_button,input_code,input_social_credit_code,
      input_social_credit_name,customs_mark,list_type,customs_declaration_date,note FROM  check_information  """)
    a = cursor.fetchall()
    # print("信息",a)


    # for i in a:
    #     print("编号",i)

    return render(request, 'show.html', {'a': a})












