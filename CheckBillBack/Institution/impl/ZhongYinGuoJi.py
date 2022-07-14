# _*_ coding: utf-8 _*_
from CheckBillBack.Institution.AbstractInstitution import AbstractInstitution
from CheckBillBack.utils.BatchDecompression import BatchDecompression


class ZhongYinGuoJi(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        if self.belong == '中银' and self.type == '普通':
            bd = BatchDecompression(file_path, file_path, ['xml'])
            bd.batchExt(pwd='29202731')