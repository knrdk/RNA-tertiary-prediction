__author__ = 'rna'

def __get_id_min_list(path):
    with open(path,'r') as f:
        data = []
        for line in f:
            (query, template, rmsd) = line.split('\t')
            data.append((query, template, float(rmsd)))
        ids = set(map(lambda x: x[0], data))

        return [
            (x,
             min([y[2] for y in data if y[0]==x]))
             # sorted([(y[1], y[2]) for y in data if y[0]==x], key = lambda x: x[1])[0])
            for x in ids]

scfg = __get_id_min_list('/home/rna/RNA/PLIKI DO PRACY/TrainingResults-1-SCFG.txt')
nw = __get_id_min_list('/home/rna/RNA/PLIKI DO PRACY/TrainingResults-1-NW.txt')

s,n,e=0,0,0
for i in range(len(scfg)):
    s_v = scfg[i][1]
    n_v = nw[i][1]
    if n_v == s_v:
        e+=1
    elif n_v < s_v:
        n+=1
    else:
        s+=1
print s,n,e