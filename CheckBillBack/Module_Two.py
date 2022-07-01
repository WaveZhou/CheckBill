# _*_ coding: utf-8 _*_
import os, datetime, shutil
from CheckBillBack.utils.Log_Record import Log
from CheckBillBack.utils.Transform_FileName import Transform_FileName
from CheckBillBack.utils.MysqlProxy import MysqlProxy
# setting = {'origin_jiuming': r'D:\估值专用邮箱数据\久铭\邮件账户分类保存\收件日20220601 当天',
#            'origin_bills': r'D:\券商对账单\origin\收件日20220601 当天'}


# 每次拷贝完一天目录下的内容，再拷贝下一天的去origin目录，要求不能重复拷贝。 直至拷贝完最近10日里的 保存目录中的内容


# 在进入这个函数前，先把源头文件和目标文件的直到当天位置的目录层次构建好并做参数传入 copy_files()

class Module_Tow(object):
    def __init__(self):
        print()

    def copy_files(self, setting,SINCE_DATE):
        if not os.path.exists(os.path.join(setting['origin_jiuming'])):
            return
        print(setting)
        for dir in os.listdir(os.path.join(setting['origin_jiuming'])):
            if os.path.isdir(os.path.join(setting['origin_jiuming'], dir)):
                for file in os.listdir(os.path.join(setting['origin_jiuming'], dir)):
                    if not os.path.exists(os.path.join(setting['origin_bills'], dir)):
                        os.makedirs(os.path.join(setting['origin_bills'], dir), exist_ok=True)
                    target_path = os.path.join(setting['origin_bills'], dir, '已处理_' + file)
                    if os.path.exists(target_path):
                        if hash(open(os.path.join(setting['origin_bills'], dir, '已处理_' + file), 'rb').read()) == hash(
                                open(os.path.join(setting['origin_jiuming'], dir, file), 'rb').read()):
                            continue
                    if file.lower().endswith('rar') or file.lower().endswith('zip'):
                        mp = MysqlProxy()
                        sql_get_record = 'SELECT * FROM `copy_record` WHERE `copy_date`=%s AND `directory`=%s AND `com_package_name`=%s'
                        one_record = mp.get_one(sql_get_record,[str(datetime.datetime.date(SINCE_DATE)),dir,file])
                        if one_record is not None:
                            continue
                        else:
                            shutil.copy(os.path.join(setting['origin_jiuming'], dir, file),
                                        os.path.join(setting['origin_bills'], dir, file))
                            sql_insert_record = 'INSERT INTO `copy_record` (`copy_date`,`directory`,`com_package_name`) VALUES (%s,%s,%s)'
                            mp.modify(sql_insert_record,[str(datetime.datetime.date(SINCE_DATE)),dir,file])
                            continue
                    # 如果文件名结尾是压缩包形式，①如果找到拷贝表中已有该日期，该目录，该压缩包的记录，则continue
                    # ②如果没找到，则拷贝一份，且在数据库拷贝表中存一条这样的记录，也continue
                    shutil.copy(os.path.join(setting['origin_jiuming'], dir, file),
                                os.path.join(setting['origin_bills'], dir, file))

    def bian_li(self, day, SINCE_DATE, basic_setting):
        for index in range(day + 1):
            jiuming = os.path.join(basic_setting['origin_jiuming'],
                                   '收件日' + ''.join(str(SINCE_DATE.date()).split('-')) + ' 当天')
            origin = os.path.join(basic_setting['origin_bills'],
                                  '收件日' + ''.join(str(SINCE_DATE.date()).split('-')) + ' 当天')
            basic_setting['origin_jiuming'] = jiuming
            basic_setting['origin_bills'] = origin

            self.copy_files(basic_setting,SINCE_DATE)

            basic_setting['origin_jiuming'] = basic_setting['origin_jiuming'].replace(
                basic_setting['origin_jiuming'].split(os.path.sep)[-1], '')
            basic_setting['origin_bills'] = basic_setting['origin_bills'].replace(basic_setting['origin_bills'].split(os.path.sep)[-1], '')
            SINCE_DATE = SINCE_DATE + datetime.timedelta(days=1)


#
# print(datetime.datetime.now().date())
# print(type(datetime.datetime.now().date()))
# print(datetime.datetime.today().date())
# # for index in range(10):

# ahh = str(res_day.date())
# print(str(res_day.date()))
# print(type(ahh))
if __name__ == '__main__':
    day_input = input('请输入要拷贝的天数：')
    input_day = int(day_input)
    SINCE_DATE_INPUT = datetime.datetime.today() - datetime.timedelta(days=input_day)
    print("从这一天起：", SINCE_DATE_INPUT.date())
    basic_setting = {'origin_jiuming': r'D:\估值专用邮箱数据\久铭\邮件账户分类保存',
                     'origin_bills': r'D:\BackUp\origin'}
    #bian_li(input_day, SINCE_DATE_INPUT, basic_setting)
    mt = Module_Tow()
    mt.bian_li(input_day,SINCE_DATE_INPUT,basic_setting)

    basic_setting = {'origin_jiuming': r'D:\估值专用邮箱数据\静久\邮件账户分类保存',
                     'origin_bills': r'D:\BackUp\origin'}
    #bian_li(input_day, SINCE_DATE_INPUT, basic_setting)
    mt.bian_li(input_day, SINCE_DATE_INPUT, basic_setting)
    log = Log('Copy_Files')
    log.show_debug('本次运行结束' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
