# _*_ coding: utf-8 _*_
from CheckBillBack.Institution.AbstractInstitution import AbstractInstitution
from CheckBillBack.utils.BatchDecompression import BatchDecompression


class NanHua(AbstractInstitution):

    def load_file_content_for_date(self, file_path: str):
        if self.belong == 'ๅๅ' and self.type == 'ๆ่ดง':
            bd = BatchDecompression(file_path, file_path, ['11650079.txt'])
            bd.batchExt()