# _*_ coding: utf-8 _*_
from CheckBillBack.Institution.AbstractInstitution import AbstractInstitution
from CheckBillBack.utils.BatchDecompression import BatchDecompression


class GuoJun(AbstractInstitution):

    def load_file_content_for_date(self, file_path:str):
        if self.belong == '国君' and self.type == '普通':
            bd = BatchDecompression(file_path, file_path, ['.xlsx'])
            bd.batchExt()
        if self.belong == '国君' and self.type == '期权':
            bd = BatchDecompression(file_path,file_path,['.pdf'])
            bd.batchExt()