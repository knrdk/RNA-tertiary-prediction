__author__ = 'Konrad Kopciuch'

from Nodes import *
from States import *

class M_cl:
    pass

class IL_cl:
    pass

class IR_cl:
    pass

class DR_cl:
    pass

class DL_cl:
    pass

class DB_cl:
    pass

gap_classes_for_node_state = {
    ROOT: {
        S : M_cl,
        IL: IL_cl,
        IR: IR_cl
    },
    BEGL: {
        S: M_cl
    },
    BEGR: {
        S: M_cl,
        IL: IL_cl
    },
    MATP: {
        MP: M_cl,
        ML: DR_cl,
        MR: DL_cl,
        D: DB_cl,
        IL: IL_cl,
        IR: IR_cl
    },
    MATL: {
        ML: M_cl,
        D: DL_cl,
        IL: IL_cl
    },
    MATR: {
        MR: M_cl,
        D: DR_cl,
        IR: IR_cl
    },
    END: {
        E: M_cl
    },
    BIF: {
        B: M_cl
    }
}