# _*_ coding: utf-8 _*_
from django.core.cache import cache
from django.db.models import Sum


import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'CheckBill.settings')
#django.setup()

from CheckBillBack.Institution.impl.DongBei import DongBei
from CheckBillBack.Module_One import ImapLoader
from CheckBillBack.structures.MailReceiveInfo import MailReceiveInfo

from MailDetail import ImapMailDetail
from CheckBillBack.structures.MailDetail import ImapMailDetail
# str = '2020-25-35'
# res = "".join(str.split('-'))
# print(res)
#self.db.session.query(ImapMailDetail).order_by('received_time').all()
#self.db.session.query(ImapMailDetail).filter_by(mail_box=folder_name, uid=uid).one()

#session.query(User).filter(User.name == 'sandy').update({"password": "foobar"}, synchronize_session="fetch")
#
# self.db.map(ImapMailInfo, ImapMailInfo.define_sqlalchemy_table(self.db.metadata))
#         self.db.map(ImapMailDetail, ImapMailDetail.define_sqlalchemy_table(self.db.metadata))
#         self.db.map(MailReceiveInfo, MailReceiveInfo.define_sqlalchemy_table(self.db.metadata))
#
# settings = {
#             'mail_bit_path': r'D:\估值专用邮箱数据\久铭\邮件IMAP二进制缓存',
#             'mail_content_path': r'D:\估值专用邮箱数据\久铭\邮件IMAP解码数据缓存',
#             'mail_classification_path': r'D:\估值专用邮箱数据\久铭\邮件账户分类保存',
#             'mail_db': r'D:\估值专用邮箱数据\久铭\估值专用邮箱缓存\jiuming_mails.db'
#         }
import json
#str_setting = json.dumps(settings)
#str_res = str_setting.encode('utf-8').decode('unicode_escape')
cache.set('jiuming_set','fsf',60 * 60 * 24)
res = cache.get('jiuming_set')
print(res)
# print(type(json.dumps(settings)))
# res = json.dumps(settings)

# decoded_u = res.encode('utf-8').decode('unicode_escape')
# print(decoded_u)




# jing_jiu = ImapLoader(settings)
# res = jing_jiu.db.session.query(MailReceiveInfo).all()
# sql = """
# INSERT INTO MailReceiveInfo (
#                                 mail_account,
#                                 institution
#                             )
#                             VALUES (
#                                 'wagwegwge.qq.com',
#                                 '共发送g给'
#                             );
# """
# mri = MailReceiveInfo()
# mri.mail_account = 'wagwegwge.qq.com'
# mri.institution = '共发送d给'
# jing_jiu.db.add(mri)
# # jing_jiu.db.execute(sql)
# # self.db.execute("""DELETE FROM `ImapMailInfo` WHERE `mail_box` = '{}' AND `uid` = '{}';""".format(folder_name, uid))
# # jing_jiu.db.execute("""INSERT INTO MailReceiveInfo VALUES ({},{})""".format('SDASGS@qq.com','周五中午'))
# print(res)









# class A:
#     def __init__(self):
#         print('hh')
#
#     def speak(self):
#         print('woqu')
# class B(A):
#     def run(self):
#         print('paoqilao')
# origin_dir = 'D:\估值专用邮箱数据\邮件账户分类缓存\收件日20220228 当天'
# tf = Transform_FileName()
# count = 0
# # for item in os.listdir(origin_dir):
# #     if os.path.isdir(os.path.join(origin_dir,item)):
# #         if tf.get_date(item) != '':
# #             for obj in os.listdir(os.path.join(origin_dir,item)):
# #                 if obj in os.listdir(origin_dir):
# #                     for file in os.listdir(os.path.join(origin_dir,item,obj)):
# #                         print(file)
# #                         count = count + 1
# #                         #shutil.move(os.path.join(origin_dir,item,obj,file),os.path.join(origin_dir,obj))
# #                         #print(obj)
# #                     #print(obj)
# # print(count)
# str = '21800108'
# res = str[0:4]
# print(res)
# xy = XingYe()
# xy.load_file_content_for_date('兴业','普通')
# DongBei

# institution_impl = locals()['DongBei']('东北', '普通')
# print(institution_impl)
# str = '国投安信期货账户'
# belong = str[0:2]
# type = str[-4:-2]
# print(belong)
# print(type)
# b = locals()['B']()
# b.speak()
# name_dict = {'zhangsan':'张三','lisi':'李四'}
# res = name_dict['zhangsan']
# print(res)
# str = '我里乖乖'
# res = str[-2:]
# print(res)
# shutil.move(os.path.join(os.path.join(origin_dir,item),obj),os.path.join(origin_dir))
# for item in os.listdir(origin_dir):
#     if os.path.isdir(os.path.join(origin_dir,item)):
#         print(item)
# os.path.join()
