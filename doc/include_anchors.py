import re
import sys
import os.path
import os


pat1a = re.compile('include::([a-zA-Z0-9_\.\-/\/]+)\_[a-zA-Z0-9]*\.py\[\]')
pat1b = re.compile('include::([a-zA-Z0-9_\.\-/\/]+)\_[a-zA-Z0-9]*\.sh\[\]')
pat1c = re.compile('include::([a-zA-Z0-9_\.\-/\/]+)\_[a-zA-Z0-9]*\.h\[\]')
pat1d = re.compile('include::([a-zA-Z0-9_\.\-/\/]+)\_[a-zA-Z0-9]*\.cpp\[\]')
pat2 = re.compile('([^@]+)@([a-zA-Z0-9]+):')
pat3 = re.compile('([^@]+)@:([a-zA-Z0-9]+)')

processed = set()

def process(root, suffix):
    #print "PROCESS ",root, suffix
    global processed
    if root in processed:
        return
    #
    anchors = {}
    anchors[''] = open('%s_.%s' % (root, suffix), 'w')
    INPUT = open('%s.%s' % (root, suffix), 'r')
    for line in INPUT:
        m2 = pat2.match(line)
        m3 = pat3.match(line)
        if m2:
            anchor = m2.group(2)
            anchors[anchor] = open('%s_%s.%s' % (root, anchor, suffix), 'w')
        elif m3:
            anchor = m3.group(2)
            anchors[anchor].close()
            del anchors[anchor]
        else:
            for anchor in anchors:
                os.write(anchors[anchor].fileno(), line)
    INPUT.close()
    for anchor in anchors:
        if anchor != '':
            print "ERROR: anchor '%s' did not terminate" % anchor
        anchors[anchor].close()
    #
    processed.add(root)


for file in sys.argv[1:]:
    print "Processing file '%s' ..." % file
    INPUT = open(file, 'r')
    for line in INPUT:
        suffix = None
        m = pat1a.match(line)
        if m:
            suffix = 'py'
        #
        if suffix is None:
            m = pat1b.match(line)
            if m:
                suffix = 'sh'
        #
        if suffix is None:
            m = pat1c.match(line)
            if m:
                suffix = 'h'
        #
        if suffix is None:
            m = pat1d.match(line)
            if m:
                suffix = 'cpp'
        #
        if not suffix is None:
            #print "HERE", line, suffix
            fname = m.group(1)+'.'+suffix
            if not os.path.exists(fname):
                print "ERROR: file '%s' does not exist!" % fname
                sys.exit(1)
            process(m.group(1), suffix)
    INPUT.close()
