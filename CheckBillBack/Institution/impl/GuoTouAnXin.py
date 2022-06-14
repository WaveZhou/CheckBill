# _*_ coding: utf-8 _*_
from CheckBillBack.Institution.AbstractInstitution import AbstractInstitution
from CheckBillBack.utils.BatchDecompression import BatchDecompression


class GuoTouAnXin(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        if self.belong == '国投' and self.type == '期货':
            bd = BatchDecompression(file_path, file_path, ['盯市'])
            bd.batchExt()
