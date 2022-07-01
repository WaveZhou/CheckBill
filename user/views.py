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
import threading


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


def job(request):
    import datetime
    cache.set("work_status", 1, 60 * 60 * 24)
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
        complete_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dict_complete = dict()
        dict_complete['code'] = '200'
        dict_complete['message'] = '第一步执行成功，最新完成时间'
        dict_complete['finish_time'] = complete_time
        cache.set("latest_finished_time", dict_complete, 60 * 60 * 24)
        cache.set("work_status", 0, 60 * 60 * 24)
        loader.log.info_running('本次运行结束', complete_time)
        return JsonResponse({'code': '200', 'message': '第一步执行成功', 'complete_time': complete_time})
    except Exception as e:
        cache.set("work_status", 0, 60 * 60 * 24)
        # NotImplementedError
        if isinstance(e, NotImplementedError):
            return JsonResponse({'code': '302', 'message': str(e)})
        else:
            logger_unknown = Log('unknown_exception')
            date_str = str(datetime.datetime.now().date())
            date_str = "".join(date_str.split('-'))
            base_dir = r'D:\整理券商对账单\bugOut'
            subject_words = '未知的异常'
            bug_out_path = os.path.join(base_dir, subject_words)
            if not os.path.exists(bug_out_path):
                os.makedirs(bug_out_path, exist_ok=True)
            bug_out_path = bug_out_path + r'\{}-log.txt'.format(date_str)
            logger_unknown.output_log({'file_name': bug_out_path, 'message': str(e)})
            return JsonResponse({'code': '302', 'message': '请去目录{}查看异常情况'.format(bug_out_path)})


def get_two_three_step_finished_time(request):
    dict_com_two = cache.get('two_step_latest_time')
    dict_com_three = cache.get('three_step_latest_time')
    info_list = list()
    if dict_com_two is not None:
        data = dict_com_two['message'] + "_" + dict_com_two['finish_time']
        info_list.append({'info_data': data})
        if dict_com_three is not None:
            data = dict_com_three['message'] + "_" + dict_com_three['finish_time']
            info_list.append({'info_data': data})
    return JsonResponse({'code': '200', 'message': info_list})


def get_init_load_finish_time(request):
    dict_com = cache.get('latest_finished_time')

    if dict_com is not None:
        if dict_com['code'] == '200':
            message = dict_com['message']
            finish_time = dict_com['finish_time']
            return JsonResponse({'code': '200', 'message': message, 'complete_time': finish_time})
        elif dict_com['code'] == '308':
            message = dict_com['message']
            finish_time = dict_com['finish_time']
            return JsonResponse({'code': '308', 'message': message, 'complete_time': finish_time})
    else:
        return JsonResponse({'code': '301', 'message': "等待第一步按钮被点击"})


import threading


class mythread(threading.Thread):

    def __init__(self, requst):
        super(mythread, self).__init__()  # 显式调用父亲的初始化函数
        self.request = requst

    def run(self):
        import schedule as sd
        d = "09:15"
        sd.every().day.at(d).do(job, self.request)
        cache.set("lock_task", 1, 60 * 60 * 1)
        # job_obj = job(request)
        while True:
            try:
                sd.run_pending()
                # print("返回值为:", job_obj)
                time.sleep(1)
            except Exception as e:
                cache.set("lock_task", 0, 60 * 60 * 1)
                dict_complete = dict()
                dict_complete['code'] = '308'
                dict_complete['message'] = '拉取邮件定时任务异常中断，中断时间'
                dict_complete['finish_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cache.set("latest_finished_time", dict_complete, 60 * 60 * 24)
                cache.set("work_status", 0, 60 * 60 * 24)
                raise e


def first_step(request):
    global res

    flag = request.GET.get("flag")
    # 第一次跑程序
    try:
        if flag != '200':
            work_status = cache.get("work_status")
            if work_status == 0 or work_status is None:
                res = job(request)
            elif work_status == 1:
                res = JsonResponse({'code': '402', 'message': "后台拉取邮件程序正在运行"})
            return res
        else:
            if cache.get("lock_task") == 1:
                res = JsonResponse({'code': '305', 'message': "后台定时任务已开启，无需重复"})
            else:
                my_lock_task = mythread(request)
                my_lock_task.start()
                res = JsonResponse({'code': '200', 'message': "后台定时任务开启成功"})
            return res
    except Exception as e:
        return JsonResponse({'code': '308', 'message': str(e)})


def two_step(request):
    # day_input = input('请输入要拷贝的天数：')
    # input_day = int(day_input)
    SINCE_DATE_INPUT = datetime.datetime.today() - datetime.timedelta(days=10)
    # print("从这一天起：", SINCE_DATE_INPUT.date())
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
    complete_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dict_complete = dict()
    dict_complete['message'] = '第二步执行成功，最新完成时间'
    dict_complete['finish_time'] = complete_time
    cache.set("two_step_latest_time", dict_complete, 60 * 60 * 24)
    return JsonResponse({'code': '200', 'message': '第二步执行成功', 'complete_time': complete_time})


def three_step(request):
    config = {
        'origin_path': r'D:\整理券商对账单\origin',
        'target_path': r'D:\整理券商对账单\target',
        'not_matched': r'D:\整理券商对账单\notMatchedFile',
        'bugOut': r'D:\整理券商对账单\bugOut'
    }
    today = datetime.datetime.today().date()
    begin_date = today - datetime.timedelta(days=10)
    three_status = cache.get("three_status")
    if three_status == 1:
        return JsonResponse({'code': '406', 'message': '后台第三步正在执行，请稍等'})
    else:
        cache.set("three_status", 1, 60 * 60 * 24)
        for i in range(11):
            print('第{}次走第三步后台函数'.format(i))
            sub_dir = '收件日' + "".join(str(begin_date).split('-')) + ' 当天'
            config['origin_path'] = os.path.join(config['origin_path'], sub_dir)
            try:
                mt = Module_Three(config)
                mt.execute()
            except Exception as e:
                if isinstance(e, FileNotFoundError):
                    begin_date += datetime.timedelta(days=1)
                    config['origin_path'] = config['origin_path'].replace(config['origin_path'].split(os.path.sep)[-1],
                                                                          '')
                    continue
                else:
                    cache.set("three_status", 0)
                    logger = Log('Unknown-Exception')
                    date_str = str(datetime.datetime.now().date())
                    date_str = "".join(date_str.split('-'))
                    base_dir = r'D:\整理券商对账单\bugOut'
                    subject_words = '未知的异常'
                    bug_out_path = os.path.join(base_dir, subject_words)
                    if not os.path.exists(bug_out_path):
                        os.makedirs(bug_out_path, exist_ok=True)
                    bug_out_path = bug_out_path + r'\{}-log.txt'.format(date_str)
                    logger.output_log({'file_name': bug_out_path, 'message': str(e)})
                    return JsonResponse({'code': '302', 'message': str(e)})
            begin_date += datetime.timedelta(days=1)
            config['origin_path'] = config['origin_path'].replace(config['origin_path'].split(os.path.sep)[-1], '')
        print(begin_date)
        complete_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print('本次处理完成 ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        dict_complete = dict()
        dict_complete['message'] = '第三步执行成功，最新完成时间'
        dict_complete['finish_time'] = complete_time
        cache.set("three_step_latest_time", dict_complete, 60 * 60 * 24)
    return JsonResponse({'code': '200', 'message': '第三步执行成功', 'complete_time': complete_time})


def re_match(request):
    # D:\整理券商对账单\notMatchedFile\20220623\对账单文件名在应到表中未匹配
    date_str = str(datetime.datetime.now().date())
    date_str = "".join(date_str.split('-'))
    base_dir = r'D:\整理券商对账单\notMatchedFile'
    target_path = os.path.join(base_dir, date_str, '对账单文件名在应到表中未匹配')
    res = os.listdir(target_path)
    cache.set("three_status", 0)
    if len(res) > 0:
        return JsonResponse({'code': '204', 'message': 'notMatchedFile目录下仍有{}个文件没有和券商账户关联'.format(len(res))})
    else:
        return JsonResponse({'code': '200', 'message': '已将近十天的对账单整理完毕，可去未到对账单页面查看结果'})
