# _*_ coding: utf-8 _*_
from CheckBillBack.Institution.AbstractInstitution import AbstractInstitution
from CheckBillBack.utils.BatchDecompression import BatchDecompression


class DongBei(AbstractInstitution):

    def load_file_content_for_date(self, file_path:str):
        if self.belong == '东北' and self.type == '普通':
            bd = BatchDecompression(file_path, file_path, ['.xls'])
            bd.batchExt()
