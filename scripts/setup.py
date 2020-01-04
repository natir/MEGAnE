#!/usr/bin/env python

'''
Copyright (c) 2020 RIKEN
All Rights Reserved
See file LICENSE for details.
'''


import os,sys,datetime,multiprocessing
from os.path import abspath,dirname,realpath,join
import log


def setup(args, base):
    log.logger.debug('started')
    # load main chrs
    global main_chrs
    if args.mainchr is not None:
        main_chr_path=args.mainchr
    else:
        main_chr_path=join(base, 'lib/human_main_chrs.txt')
    main_chrs=[]
    with open(main_chr_path) as infile:
        for line in infile:
            chr=line.strip()
            if not chr == '':
                main_chrs.append(chr)
    if args.mainchr is None:
        if args.gender == 'female':
            main_chrs=main_chrs[:-1]
            print('You specified "female" as gender, chrY was excluded.')

    # load parameter settings
    global params
    if args.setting is not None:
        param_path=args.setting
    else:
        param_path=join(base, 'lib/parameter_settings.txt')
    import load_parameters
    params=load_parameters.load(param_path)

    # load rep headers to be removed
    global rep_headers_to_be_removed
    if args.repremove is not None:
        param_path=args.repremove
    else:
        param_path=join(base, 'lib/non_ME_rep_headers.txt')
    rep_headers_to_be_removed=set()
    with open(param_path) as infile:
        for line in infile:
            line=line.strip().replace(' ', '_')
            if not line == '':
                rep_headers_to_be_removed.add(line)

    # load rep with polyA tail
    global rep_with_pA
    if args.pA_ME is not None:
        param_path=args.pA_ME
    else:
        param_path=join(base, 'lib/ME_with_polyA_tail.txt')
    rep_with_pA=set()
    with open(param_path) as infile:
        for line in infile:
            line=line.strip().replace(' ', '_')
            if not line == '':
                rep_with_pA.add(line)
