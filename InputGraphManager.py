def setDemFileName(inputgraph, demfile):
    targetidx = 0
    with open(inputgraph, 'r') as fin:
        lines = fin.readlines()
    for idx, l in enumerate(lines):
        if 'demFileName' in l:
            targetidx = idx
            break
    lines[targetidx] = '\t\tdemFileName '+demfile
    print lines
    with open(inputgraph, 'w') as fout:
        fout.writelines(lines)
