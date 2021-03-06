# _*_ coding: utf-8 _*_
from CheckBillBack.Institution.AbstractInstitution import AbstractInstitution
from CheckBillBack.utils.BatchDecompression import BatchDecompression


class ChangJiang(AbstractInstitution):

    def load_file_content_for_date(self, file_path:str):
        if self.belong == '长江' and self.type == '期货':
            bd = BatchDecompression(file_path, file_path, ['550825.txt','550826.txt'])
            bd.batchExt()
