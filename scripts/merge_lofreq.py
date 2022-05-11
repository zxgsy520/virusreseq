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


def read_lofreq_cvf(file):

    r = {}

    for line in read_tsv(file, "\t"):
        if line[0] not in r:
            r[line[0]] = {}
        r[line[0]][int(line[1])] = [line[3], line[4]]

    return r


def get_prefix(file):

    file = file.split("/")[-1]

    if "." in file:
        prefix = file.split(".")[0]
    else:
        prefix = file

    return prefix


def merge_lofreq(files):

    data = {}
    indexs = {}
    samples = []

    for file in files:
        prefix = get_prefix(file)
        if "_" in prefix:
            prefix = prefix.split("_", 1)[-1]
        samples.append(prefix)

        r = read_lofreq_cvf(file)
        data[prefix] = r
        for i in r:
            if i not in indexs:
                indexs[i] = set()
            indexs[i] = indexs[i] | set(r[i].keys())

    print("#CHROM\tPOS\tREF\t%s" % "\t".join(samples))
    fo = open("lofreq_distribution.tsv", "w")
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
        help="Input the snp result of lofreq analysis,(*.vcf)")

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
        merge_lofreq.py *.vcf > merge_lofreq_vcf.tsv

version: %s
contact:  %s <%s>\
    ''' % (__version__, " ".join(__author__), __email__))

    args = add_hlep_args(parser).parse_args()

    merge_lofreq(args.input)


if __name__ == "__main__":

    main()
