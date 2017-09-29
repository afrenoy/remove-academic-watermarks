#!/usr/bin/env python3
import sys
import os
import textwrap


def containspattern(l, patterns):
    for p in patterns:
        if p.encode() in l:
            return True


def cleanpdf(source, destination, patterns):
    f = open(source, 'r+b')
    lines = f.readlines()
    f.close()

    alloccurences = [n for (n, l) in enumerate(lines) if containspattern(l, patterns)]
    toremove = []

    for n in alloccurences:
        begin = None
        i = n
        while i > 0 and not begin:
            i = i-1
            if 'BT'.encode() in lines[i]:
                begin = i
        if not begin:
            sys.exit('Beginning not found')
        end = None
        j = n
        while j < len(lines)-2 and not end:
            j = j+1
            if 'ET'.encode() in lines[j]:
                end = j
        if not end:
            sys.exit('End not found')
        # Replace by blank lines
        toremove.append((begin, end))  # So far we just add the lines to be removed to the list. The removal is only performed after all occurences have been treated, avoiding problems in case several occurences are found in the same block.

    bytesremoved = 0
    for (begin, end) in toremove:
        for k in range(begin, end+1):
            size = len(lines[k])
            bytesremoved = bytesremoved + size
            lines[k] = ''.encode()

    if bytesremoved > 0:  # If no watermark was found, we don't write any output
        g = open(destination, 'w+b')
        for l in lines:
            g.write(l)
        g.close()
    return(bytesremoved, len(toremove))


if len(sys.argv) < 4:
    line1 = "usage: %s inputfile outputfile pattern1 ... patternN" % sys.argv[0]
    line2 = textwrap.fill("This program searches for specific text strings in a pdf, and removes the blocks containing them. It can thus remove many of the 'watermarks' used by academic publishers to identify who downloaded the pdf from the paywall, provided common text found in these watermarks is given as arguments. The only dependency is pdftk, used to uncompress the pdf.", width=100)
    line3 = "If you want to update the pdf instead of creating a new one, you can provide the same value for inputfile and outputfile"
    line4 = "Example: %s Lowry1951.pdf Lowry1951-clean.pdf 'EIDGENOESSISCHE TECHNISCHE HOCHSCHULE' 'Downloaded from' 'Access provided' 'For personal use only' '129.132.214.233'" % sys.argv[0]
    sys.exit(line1 + '\n\n' + line2 + '\n\n' + line3 + '\n\n' + line4)

source = sys.argv[1]
destination = sys.argv[2]
patterns = sys.argv[3:]

es = os.system('pdftk %s output %s uncompress' % (source, source+'-tmp'))
if es != 0:
    sys.exit('Failed to uncompress the pdf')

(bytesremoved, nremoved) = cleanpdf(source+'-tmp', destination+'-tmp', patterns)
if nremoved > 0:
    es = os.system('pdftk %s output %s compress' % (destination+'-tmp', destination))
    if es != 0:
        sys.exit('Failed to compress the pdf')

    os.remove(source+'-tmp')
    if source != destination:
        os.remove(destination+'-tmp')
    print('Found %d patterns in file %s, removing %d bytes' % (nremoved, source, bytesremoved))
else:
    os.remove(source+'-tmp')

