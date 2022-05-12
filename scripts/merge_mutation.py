#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import gzip
import logging
import argparse

from collections import OrderedDict

LOG = logging.getLogger(__name__)

__version__ = "1.0.0"
__author__ = ("Xingguo Zhang",)
__email__ = "invicoun@foxmail.com"
__all__ = []


def read_tsv(file, sep=None):

    LOG.info("reading message from %r" % file)

    if file.endswith(".gz"):
        fp = gzip.open(file)
    else:
        fp = open(file)

    for line in fp:
        if isinstance(line, bytes):
            line = line.decode("utf-8")
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        yield line.split(sep)

    fp.close()


def get_mutated_base(ref, nutlist):

    data = {1:"A", 2:"C", 3:"G", 4:"T"}

    r = ""
    n = 0
    for i in nutlist:
        n += 1
        alt = data[n]
        if alt == ref:
            continue
        if float(i) <= 0:
            continue
        r = "%s,%s" % (r, alt)

    return r.strip(",")


def read_mutation_table(file, freq=0):

    r = {}

    for line in read_tsv(file, "\t"):
        if float(line[9]) <= freq:
            continue
        if line[0] not in r:
            r[line[0]] = {}
        ref = line[2].upper()
        alt = get_mutated_base(ref, line[5:9])
        r[line[0]][int(line[1])] = [ref, alt]

    return r


def get_prefix(file):

    file = file.split("/")[-1]

    if "." in file:
        prefix = file.split(".")[0]
    else:
        prefix = file

    return prefix


def merge_mutation(files, freq=0):

    data = {}
    indexs = {}
    samples = []

    for file in files:
        prefix = get_prefix(file)
        if "_" in prefix:
            prefix = prefix.split("_", 1)[-1]
        samples.append(prefix)

        r = read_mutation_table(file, freq)
        data[prefix] = r
        for i in r:
            if i not in indexs:
                indexs[i] = set()
            indexs[i] = indexs[i] | set(r[i].keys())

    print("#CHROM\tPOS\tREF\t%s" % "\t".join(samples))
    fo = open("mutation_distribution.tsv", "w")
    fo.write("ID\t%s\n" % "\t".join(samples))

    for i in indexs:
        sitlist = list(indexs[i])
        for j in sorted(sitlist):
            ref = ""
            temp = []
            temp1 = []
            for s in samples:
                if s not in data:
                    temp.append(".")
                    temp1.append("0")
                    continue
                if i not in data[s]:
                    temp.append(".")
                    temp1.append("0")
                    continue
                if j not in data[s][i]:
                    temp.append(".")
                    temp1.append("0")
                    continue
                ref, alt = data[s][i][j]
                temp.append(alt)
                temp1.append("1")
            print("%s\t%s\t%s\t%s" % (i, j, ref, "\t".join(temp)))
            fo.write("%s_%s-%s\t%s\n" % (i, j, ref, "\t".join(temp1)))
    fo.close()

    return 0


def add_hlep_args(parser):

    parser.add_argument("input", nargs="+", metavar="FILE", type=str,
        help="Input mutation rate statistics file.")
    parser.add_argument("-f", "--freq", metavar="FLOAT", type=float, default=0,
        help="Input the filtered mutation frequency(‰). freq=0")

    return parser


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''
For exmple:
        merge_mutation.py *.mutation.xls > merge_mutation.xls

version: %s
contact:  %s <%s>\
    ''' % (__version__, " ".join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    merge_mutation(args.input, args.freq)


if __name__ == "__main__":

    main()
