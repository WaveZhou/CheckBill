import datetime
import os
import pickle
import time

import schedule
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import HttpResponse
# Create your views here.
from CheckBillBack.Module_One import ImapLoader
from CheckBillBack.Module_Three import Module_Three
from CheckBillBack.Module_Two import Module_Tow
from CheckBillBack.utils.Log_Record import Log
from user.models import Profile

from .models import Profile


def add_person(request):
    zhangsan = Profile(user_id=11, user_name='张三', user_phone='13548495217', user_email='zhangsan2551@163.com',
                       is_autorized=1)
    # xu2 = Persion(first_name='徐',last_name='二')
    zhangsan.save()
    # xu2.save()
    # person1 = Persion(first_name='张',last_name='三')
    # person1.save()
    # person2 = Persion()
    # person2.first_name = '李'
    # person2.last_name = '四'
    # person2.save()
    # wangwu = Persion.objects.create(first_name='王',last_name='五')
    # zhaoliu = Persion.objects.get_or_create(first_name='赵',last_name='六')
    return HttpResponse('添加数据成功')


def get_person(request):
    from utils import MysqlProxy
    token = request.GET.get('token')
    print(type(cache.get('login_user')))
    global login_user
    try:
        for item in cache.get('login_user'):
            if item[token] != None:
                login_user = item[token]
    except KeyError:
        return JsonResponse({'status_code': '304', 'message': "登录已失效或被刷掉，请先登录"})
    if login_user == None:
        return JsonResponse({'status_code': '302', 'message': "请先登录"})
    user_id = login_user.user_id
    mq = MysqlProxy.MysqlProxy()
    user_list = mq.get_list("select * from jm_statement.user_profile where user_id=%s", [int(user_id)])
    # print(user_list[0])
    # print(type(user_list[0]))
    mq.close()
    return JsonResponse({'status_code': '200', 'user_obj': user_list[0], 'token': token})


def save_pagesize(request):
    global login_user
    from utils import MysqlProxy
    print("==============保存页码==================", end="")
    pagesize = request.GET.get("pagesize")
    login_user_list = cache.get('login_user')
    token = request.GET.get("token")
    for ele in login_user_list:
        if ele[token] != None:
            login_user = ele[token]
    if login_user == None:
        return JsonResponse({'code': '300', 'message': '保存失败，请先登录'})
    user_id = login_user.user_id
    sql = "UPDATE jm_statement.`user_profile` SET `page_size` = %s WHERE `user_id` = %s"
    mq = MysqlProxy.MysqlProxy()
    mq.modify(sql, [int(pagesize), int(user_id)])
    print(pagesize)
    return JsonResponse({'code': '200', 'message': '保存成功', 'token': token})


# def update_person(request):
#     #根据条件查询后再修改和保存
#     # zhangsan = Persion.objects.get(first_name='张')
#     # zhangsan.last_name='三丰'
#     # zhangsan.save()
#     #直接修改所有数据
#     Persion.objects.all().update(first_name='雷')
#     return HttpResponse('修改数据成功')
# def delete_person(request):
#     Persion.objects.get(last_name='三丰').delete()
#     return HttpResponse('数据删除成功')
# def login(request):
#     username = request.POST.get("username")
#     password = request.POST.get("password")
#     print("username:"+str(username))
#     print("password:"+str(password))
#     try:
#         user = Person.objects.get(first_name=username)
#     except:
#         date = {'flag': 'no', "msg": "no to user"}
#         return JsonResponse({'request': date})
#     if password == user.last_name:
#         date_msg = "登陆成功"
#         date_flag = "yes"
#         print("成功")
#     else:
#         date_msg = "密码输入错误"
#         date_flag = "no"
#     date = {'flag': date_flag, 'msg': date_msg}
#     return JsonResponse({'request': date})
def job(request):
    import datetime
    SINCE_DATE = datetime.date.today() - datetime.timedelta(days=5)
    try:
        settings = {
            'mail_bit_path': r'D:\估值专用邮箱数据\久铭\邮件IMAP二进制缓存',
            'mail_content_path': r'D:\估值专用邮箱数据\久铭\邮件IMAP解码数据缓存',
            'mail_classification_path': r'D:\估值专用邮箱数据\久铭\邮件账户分类保存',
            'mail_db': r'D:\估值专用邮箱数据\久铭\估值专用邮箱缓存\jiuming_mails.db'
        }
        settings.update(
            pickle.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jiuming.pick'), 'rb')))
        loader = ImapLoader(settings)
        loader.update_mail_data_base(
            since_date=SINCE_DATE,
            # since_date=datetime.date(2019, 10, 20),
            # on_date=datetime.date(2019, 10, 20),
        )
        loader.update_mail_content_cache()

        loader.update_mail_classification(
            folder_tag='久铭',
            range_start=SINCE_DATE,
            # range_start=datetime.date(2019, 10, 20),
            # range_end=datetime.date(2019, 9, 6),
        )

        settings = {
            'mail_bit_path': r'D:\估值专用邮箱数据\静久\邮件IMAP二进制缓存',
            'mail_content_path': r'D:\估值专用邮箱数据\静久\邮件IMAP解码数据缓存',
            'mail_classification_path': r'D:\估值专用邮箱数据\静久\邮件账户分类保存',
            'mail_db': r'D:\估值专用邮箱数据\静久\估值专用邮箱缓存\jingjiu_mails.db'
        }
        settings.update(pickle.load(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'jjkm.pick'), 'rb')))

        loader = ImapLoader(settings)
        loader.update_mail_data_base(
            since_date=SINCE_DATE,
            # since_date=datetime.date(2019, 10, 20),
            # on_date=datetime.date(2019, 10, 20),
        )
        loader.update_mail_content_cache()
        loader.update_mail_classification(
            folder_tag='静久',
            range_start=SINCE_DATE,
            # range_start=datetime.date(2019, 10, 20),
            # range_end=datetime.date(2019, 9, 6),
        )

        loader.log.info_running('本次运行结束', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return JsonResponse({'code': '200', 'message': '第一步执行成功'})
    except Exception as e:
        if request.GET.get('flag') != 200:
            raise e
            # return JsonResponse({'code': '302', 'message': str(e)})
        else:
            raise e


def first_step(request):
    import schedule as sd

    flag = request.GET.get("flag")
    # 第一次跑程序
    if flag != '200':
        res = job(request)
    else:
        # res = job(request)
        d = "09:15"
        sd.every().day.at(d).do(job, request)
        # job_obj = job(request)
        while True:
            try:
                sd.run_pending()
                # print("返回值为:", job_obj)
                time.sleep(1)
            except Exception as e:
                return JsonResponse({'code': '302', 'message': str(e)})

    return res


def two_step(request):
    #day_input = input('请输入要拷贝的天数：')
    #input_day = int(day_input)
    SINCE_DATE_INPUT = datetime.datetime.today() - datetime.timedelta(days=10)
    print("从这一天起：", SINCE_DATE_INPUT.date())
    basic_setting = {'origin_jiuming': r'D:\估值专用邮箱数据\久铭\邮件账户分类保存',
                     'origin_bills': r'D:\整理券商对账单\origin'}
    # bian_li(input_day, SINCE_DATE_INPUT, basic_setting)
    mt = Module_Tow()
    mt.bian_li(10, SINCE_DATE_INPUT, basic_setting)
    basic_setting = {'origin_jiuming': r'D:\估值专用邮箱数据\静久\邮件账户分类保存',
                     'origin_bills': r'D:\整理券商对账单\origin'}
    # bian_li(input_day, SINCE_DATE_INPUT, basic_setting)
    mt.bian_li(10, SINCE_DATE_INPUT, basic_setting)
    log = Log('Copy_Files')
    log.show_debug('本次运行结束' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    return JsonResponse({'code': '200', 'message': '第二步执行成功'})


def three_step(request):
    config = {
        'origin_path': r'D:\整理券商对账单\origin',
        'target_path': r'D:\整理券商对账单\target',
        'not_matched': r'D:\整理券商对账单\notMatchedFile',
        'bugOut': r'D:\整理券商对账单\bugOut'
    }
    today = datetime.datetime.today().date()
    begin_date = today - datetime.timedelta(days=10)
    print(begin_date)
    for i in range(11):
        sub_dir = '收件日' + "".join(str(begin_date).split('-')) + ' 当天'
        config['origin_path'] = os.path.join(config['origin_path'],sub_dir)
        try:
            mt = Module_Three(config)
            mt.execute()
        except Exception as e:
            if isinstance(e,FileNotFoundError):
                continue
            else:
                return JsonResponse({'code': '302', 'message': str(e)})
        begin_date += datetime.timedelta(days=1)
        config['origin_path'] = config['origin_path'].replace(config['origin_path'].split(os.path.sep)[-1],'')
    print(begin_date)
    print('本次处理完成 ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    return JsonResponse({'code': '200', 'message': '第三步执行成功'})
