import yapsy.IPlugin  :: * ;
import ruamel.yaml :: * ;
import typing :: * ;
import uatg.regex_formats as rf
import re
import os
import random   

class set_thrashing(IPlugin):
    sets = 64
    word_size = 8
    block_size = 8
    ways = 4
    fb_size = 9
    
    def _init_(self):
        super()._init_()
        
    def execute(self, core_yaml, isa_yaml):
        _dcache_dict = core_yaml['dcache_configuration']
        _dcache_en = _dcache_dict['instantiate']
        self._sets = _dcache_dict['sets']
        self._word_size = _dcache_dict['word_size']
        self._block_size = _dcache_dict['block_size']
        self._ways = _dcache_dict['ways']
        self._fb_size = _dcache_dict['fb_size']

    def check_log(self, log_file_path, reports_dir):
        f = open(log_file_path, "r")
        log_file = f.read()
        f.close()

        test_report = {
                "cache_fill_load": {
                    'Doc': "ASM should have filled the buffer of size".format(self._fb_size)
                    'Execution status': ''
                    }
                }


    def generate_asm(self) -> List[Dict[str, Union[Union[str, list], Any]]]:

        asm_data = '\nrvtest_data:\n'

        for i in range (self._block_size * self._sets * self._ways*2):
            asm_data += "\t.word 0x{0:08x}\n".format(random.randrange(16**8))

    	asm_main = "\n\tfence\n\t\n\tli t0, 69\n\tli t1, 1\n\tli t3, {0}\n\tla t2, rvtest_data".format(self._sets, self._ways)
        asm_lab1 = "lab1:\n\tsw t0, 0(t2)\n\taddi t2, t2, {0}\n\tbeq t4, t3, nop\n\taddi t4, t4, 1\n\tj lab1".format(self._block_size * self._word_size)
        asm_nop = "nop:\n\tmv t4, x0\n"
        for i in range(self._fb_size * 2):
            asm_nop += "\tnop\n"

        asm_st = "asm_st:\n"
        for i in range(100)
            asm_st += "\tlw, {0}(t2)".format(i*(self._word_size*self._block_size*self._sets))
        asm_end = "\nend:\n\tnop\n\tfence.i\n"
	    asm = asm_main + asm_lab1 + asm_nop + asm_st + asm_end
        compile_macros = []    	
    	
    	return [{
            'asm_code': asm,
            'asm_data': asm_data,
            'asm_sig': '',
            'compile_macros': compile_macros
        }]
