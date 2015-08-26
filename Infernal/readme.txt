To calculate sequence percent identity using Infernal, first align the sequences of interest to the same model using 'cmalign'. Then use the 'esl-alipid' utility program that is included with Infernal here <PATH-TO-INFERNAL-1.1.1>/easel/miniapps/esl-alipid. For example:

> /src/infernal-1.1.1/src/cmalign my.cm my.fa > my.stk

> /src/infernal-1.1.1/easel/miniapps/esl-alipid my.stk