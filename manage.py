#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.cache import cache

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CheckBill.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    # settings = {
    #             'mail_bit_path': r'D:\估值专用邮箱数据\久铭\邮件IMAP二进制缓存',
    #             'mail_content_path': r'D:\估值专用邮箱数据\久铭\邮件IMAP解码数据缓存',
    #             'mail_classification_path': r'D:\估值专用邮箱数据\久铭\邮件账户分类保存',
    #             'mail_db': r'D:\估值专用邮箱数据\久铭\估值专用邮箱缓存\jiuming_mails.db'
    #         }
    # cache.set('jiuming_set', settings, 60 * 60 * 24)
    # res = cache.get('jiuming_set')
    # print(res)

if __name__ == '__main__':
    main()
