import json
import openpyxl
import os

from django.http import JsonResponse, request
from django.core.cache import cache
from CheckBillBack.Module_One import ImapLoader
from CheckBillBack.structures.MailReceiveInfo import MailReceiveInfo
from sqlalchemy.orm.exc import NoResultFound


def get_print_bills(request):
    # 处理前端发来的post请求里的print_list
    choice_time = request.GET.get("choice_time")
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = '未到对账单账户信息'
    sheet['A1'] = '产品名称'
    sheet['B1'] = '券商'
    sheet['C1'] = '账户类型'
    sheet['D1'] = '账户号'
    sheet['E1'] = '上海卡号'
    sheet['F1'] = '深圳卡号'
    sheet['G1'] = '开户日期'
    sheet['H1'] = '所属营业部'
    sheet['I1'] = '联系人'
    sheet['J1'] = '邮箱'
    sheet['K1'] = '手机'
    sheet['L1'] = '电话'
    sheet['M1'] = '微信'
    if os.path.exists(choice_time + "未到对账单账户信息.xlsx"):
        os.remove(choice_time + "未到对账单账户信息.xlsx")
    store_list = list()

    # print(choice_time)
    json_str = request.body
    json_dict_list = json.loads(json_str)
    for dl in json_dict_list:
        store_list.append(
            [dl['product'], dl['belong'], dl['type'], dl['account'], dl['card_sh'], dl['card_sz'], dl['start_date'],
             dl['business_department'], dl['contacts'], dl['contact_email'], dl['contact_mob'], dl['contact_tel'],
             dl['contact_weixin']])
    for i in store_list:
        sheet.append(i)
    # datetime.datetime.today().date().strftime("%Y-%m-%d")
    # sub_dir = "frontport/dist/static/"
    sub_dir = "static/"
    # sub_dir_back = "CheckBill/static/"
    sub_dir_front = "frontport/dist/static/"

    save_dir = os.path.join(os.getcwd(), sub_dir_front)
    file_name = "未到对账单账户信息{0}.xlsx".format(choice_time)
    save_unit = save_dir + file_name
    wb.save(save_unit)
    url = "http://192.168.1.151:8000/" + sub_dir + file_name
    # url = 'http://192.168.1.151:8000/'+
    # #applicationnd.openxmlformats-officedocument.spreadsheetml.sheet
    # response = HttpResponse(content=save_virtual_workbook(wb),content_type='applicationnd.openxmlformats-officedocument.spreadsheetml.sheet')
    # # 给返回的文件命名
    # response['Content-Disposition'] = 'attachment; filename={0}.xlsx'.format(quote(str(choice_time+"未到对账单账户信息")))  # 中文名字
    # #syts = os.getcwd()+"\\" +choice_time+"未到对账单账户信息.xlsx"
    # response['urls'] = syts
    # print(syts)
    # JsonResponse({'status':'200','res_url':syts})
    return JsonResponse({'code': 200, 'url': url})


def get_email_config(request):
    jiuming_settings = {
        'mail_bit_path': r'D:\估值专用邮箱数据\久铭\邮件IMAP二进制缓存',
        'mail_content_path': r'D:\估值专用邮箱数据\久铭\邮件IMAP解码数据缓存',
        'mail_classification_path': r'D:\估值专用邮箱数据\久铭\邮件账户分类保存',
        'mail_db': r'D:\估值专用邮箱数据\久铭\估值专用邮箱缓存\jiuming_mails.db'
    }
    jingjiu_settings = {
        'mail_bit_path': r'D:\估值专用邮箱数据\静久\邮件IMAP二进制缓存',
        'mail_content_path': r'D:\估值专用邮箱数据\静久\邮件IMAP解码数据缓存',
        'mail_classification_path': r'D:\估值专用邮箱数据\静久\邮件账户分类保存',
        'mail_db': r'D:\估值专用邮箱数据\静久\估值专用邮箱缓存\jingjiu_mails.db'
    }
    cache.set("jiuming_set", jiuming_settings, 60 * 60 * 24)
    cache.set("jingjiu_set", jingjiu_settings, 60 * 60 * 24)
    imapLoad_jiuming = ImapLoader(jiuming_settings)
    imapload_jingjiu = ImapLoader(jingjiu_settings)
    res_jiuming = imapLoad_jiuming.db.session.query(MailReceiveInfo).all()
    res_jingjiu = imapload_jingjiu.db.session.query(MailReceiveInfo).all()
    imapLoad_jiuming.db.close()
    imapload_jingjiu.db.close()
    result_list_jiuming = list()
    result_list_jingjiu = list()
    for ele in res_jingjiu:
        obj = dict()
        if isinstance(ele, MailReceiveInfo):
            obj['mail_account'] = ele.mail_account
            obj['institution'] = ele.institution
        result_list_jingjiu.append(obj)
    for ele in res_jiuming:
        obj = dict()
        if isinstance(ele, MailReceiveInfo):
            obj['mail_account'] = ele.mail_account
            obj['institution'] = ele.institution
        result_list_jiuming.append(obj)
    return JsonResponse(
        {'status_code': 200, 'result_list_jiuming': result_list_jiuming, 'result_list_jingjiu': result_list_jingjiu})


def util_add_config(request, imapLoad):
    if request.method == 'POST':
        post_body = json.loads(request.body.decode())
        try:
            mailReceiveInfo = imapLoad.db.session.query(MailReceiveInfo).filter_by(
                mail_account=post_body['mail_account'], institution=post_body['institution']).one()
            return JsonResponse({'status_code': 302,
                                 'message': '已存在该邮箱号{}和机构名称{}配置'.format(mailReceiveInfo.mail_account,
                                                                        mailReceiveInfo.institution)})
        except NoResultFound:
            mri = MailReceiveInfo()
            mri.mail_account = post_body['mail_account']
            mri.institution = post_body['institution']
            imapLoad.db.add(mri)
            imapLoad.db.close()


def add_email_config(request):
    # 先查询数据库中是否已经存在这个配置的记录，已存在，则新增不成功
    # self.db.session.query(ImapMailDetail).filter_by(mail_box=folder_name, uid=uid).one()
    global imapLoad
    flag = request.GET.get("flag")
    try:
        if flag == '1':
            settings = cache.get("jiuming_set")
            imapLoad = ImapLoader(settings)
        elif flag == '2':
            settings = cache.get("jingjiu_set")
            imapLoad = ImapLoader(settings)
        util_add_config(request, imapLoad)
    except Exception as e:
        return JsonResponse({'status_code': 302, 'message': str(e)})

    return JsonResponse({'status_code': 200, 'message': '新增成功'})


def search_eamil_config(imapLoad, key_words):
    sql = "SELECT * FROM `MailReceiveInfo` WHERE `mail_account` like {} or `institution` like  {}".format(
        "'%%" + key_words + "%%'", "'%%" + key_words + "%%'")
    sqlite_con = imapLoad.sqlite3_con
    cursor = sqlite_con.cursor()
    res = cursor.execute(sql)
    result_list = list()
    for ele in res:
        tem_dict = dict()
        tem_dict['mail_account'] = ele[0]
        tem_dict['institution'] = ele[1]
        result_list.append(tem_dict)
    sqlite_con.close()
    imapLoad.db.close()
    return result_list


def search_jiuming(request):
    try:
        key_words = request.GET.get("search_words")
        settings = cache.get("jiuming_set")
        imapLoad = ImapLoader(settings)
        result_list = search_eamil_config(imapLoad, key_words)
    except Exception as e:
        return JsonResponse({'status_code': 302, 'message': str(e)})
    return JsonResponse({'status_code': 200, 'message': '查询成功', 'result_list': result_list})


def search_jingjiu(request):
    try:
        key_words = request.GET.get("search_words")
        settings = cache.get("jingjiu_set")
        imapLoad = ImapLoader(settings)
        result_list = search_eamil_config(imapLoad, key_words)
    except Exception as e:
        return JsonResponse({'status_code': 302, 'message': str(e)})
    return JsonResponse({'status_code': 200, 'message': '查询成功', 'result_list': result_list})


def update_config(imapLoader, mail_to, inst_to, mail_con, inst_con):
    sqlite3_con = imapLoader.sqlite3_con
    sql = "UPDATE `MailReceiveInfo` SET `mail_account` = '{}',`institution` = '{}' WHERE `mail_account` = '{}' AND `institution` = '{}';".format(
        mail_to, inst_to, mail_con, inst_con)
    cursor = sqlite3_con.cursor()
    cursor.execute(sql)
    sqlite3_con.commit()
    sqlite3_con.close()
    imapLoader.db.close()


def update_jiuming_email_config(request):
    try:
        if request.method == 'POST':
            post_body = json.loads(request.body.decode())
            mail_to = post_body['mail_account']
            inst_to = post_body['institution']
            res_condition = post_body['edit_condition']
            mail_con = str(res_condition).split("_")[0]
            inst_con = str(res_condition).split("_")[1]
            flag = str(res_condition).split("_")[2]
            if flag == '1':
                settings = cache.get("jiuming_set")
                imapLoader = ImapLoader(settings)
                update_config(imapLoader, mail_to, inst_to, mail_con, inst_con)
            elif flag == '2':
                settings = cache.get("jingjiu_set")
                imapLoader = ImapLoader(settings)
                update_config(imapLoader, mail_to, inst_to, mail_con, inst_con)
    except Exception as e:
        return JsonResponse({'status_code': 302, 'message': str(e)})
    return JsonResponse({'status_code': 200, 'message': '数据修改成功'})


def delete_email_config(imapLoader, mail_account, institution):
    sqlite3_con = imapLoader.sqlite3_con
    cursor = sqlite3_con.cursor()
    sql = "DELETE FROM `MailReceiveInfo` WHERE `mail_account` = '{}' AND `institution` = '{}'".format(mail_account,
                                                                                                      institution)
    cursor.execute(sql)
    sqlite3_con.commit()
    sqlite3_con.close()
    imapLoader.db.close()


def delete_jiuming_email_config(request):
    global imapLoader
    try:
        flag = request.GET.get("flag")
        mail_account = request.GET.get("mail_account")
        institution = request.GET.get("institution")
        if flag == '1':
            settings = cache.get("jiuming_set")
            imapLoader = ImapLoader(settings)
        elif flag == '2':
            settings = cache.get("jingjiu_set")
            imapLoader = ImapLoader(settings)
        delete_email_config(imapLoader, mail_account, institution)
    except Exception as e:
        return JsonResponse({'status_code': 302, 'message': str(e)})
    return JsonResponse({'status_code': 200, 'message': '数据删除成功'})

# def get_excel(request):
#     print("66666666666666666")
#     a = "CheckBill/static/"
#     save_path = a + "未到对账单账户信息{0}.xlsx".format("2021-11-01")
#     url = "http://192.168.1.151:8000/"+save_path
#     print(url)
#     response = {
#         'url':url,
#     }
#     return HttpResponse(json.dumps(response))
# def export_data(request):
#
#     wb = openpyxl.Workbook()
# 	'''
# 	....为写入数据的步骤 略
# 	'''
#
# 	# 吧文件流写入 返回体
#     response = HttpResponse(content=save_virtual_workbook(wb),
#                             content_type='applicationnd.openxmlformats-officedocument.spreadsheetml.sheet')
#     # 给返回的文件命名
#     response['Content-Disposition'] = 'attachment; filename={0}.xlsx'.format(quote(str(title)))  # 中文名字
#
#     return response

