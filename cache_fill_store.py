import yapsy.IPlugin  :: * ;
import ruamel.yaml :: * ;
import typing :: * ;
import uatg.regex_formats as rf
import re
import os
import random   

class cache_fill_store(IPlugin):
  
    def __init__(self):

        super().__init__()

    def execute(self, core_yaml, isa_yaml):
 
        _dcache_dict = core_yaml['dcache_configuration']
        _dcache_en = _dcache_dict['instantiate']
        self._sets = _dcache_dict['sets']
        self._word_size = _dcache_dict['word_size']
        self._block_size = _dcache_dict['block_size']
        self._ways = _dcache_dict['ways']
        self._cache_size=self._sets*self._ways*self._block_size
        self._fb_size=_dcache_dict['fb_size']
        return True

    def generate_asm(self) -> List[Dict[str, str]]:
 
        asm_data = '\nrvtest_data:\n'

        for i in range (self._cache_size*4):
            val=str(hex(int(random.uniform(0,self._cache_size*4)))[2:].zfill(8))
            asm_data+=f"\t.word 0x{val}\n"


        asm='init:\n\tfence\n\tli t0, 501\n\tli t2,32\n\tla t1, rvtest_data\n'
        
 
        asm+='fillc:'
        for i in range(self._cache_size):
            asm+=f'\n\tlw t0, 0(t1)\n\taddi t1, t1, {self._sets*self._block_size*self._word_size}\n'
        
 
        asm+='clearfb:'
        for i in range(30):
            asm+='\n\tnop\n'


        asm+='fillfb:'
        for i in range(self._fb_size//2):
            asm+='\n\taddi t1, t1, 32\n\tlw t0, 0(t1)\n'


        asm+='hits:'
        for i in range(self._fb_size//2):
            asm+='\n\tlw t0,0(t1)\n\tsub t1,t1,t2\n'

        asm+='end:\n\tnop\n'


        return [{
            'asm_code': asm,
            'asm_data': asm_data,
            'asm_sig': '',
            'compile_macros': []
        }]

    def check_log(self, log_file_path, reports_dir):
        return None

    def generate_covergroups(self, config_file):
        return ''
