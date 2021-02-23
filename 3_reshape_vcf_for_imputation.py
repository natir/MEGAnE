#!/usr/bin/env python

'''
Copyright (c) 2020 RIKEN
All Rights Reserved
See file LICENSE for details.

Prerequisite: Python3.7

Usage: python %prog -i input_MEI_jointcall.vcf(.gz) -a input_MEA_jointcall.vcf(.gz) -n cohort_name

Usage details:
- "input_MEI_jointcall.vcf(.gz)" and "input_MEA_jointcall.vcf(.gz)" must be generated by joint calling pipeline of MEGAnE (the 2nd step).
- This script merged two VCF files: a joint-called VCF of MEIs and VCF of a joint-called VCF of absent MEs. This script cannot merge individual-level VCF files.
- This script not only merges two VCF, but also removes multi-allelic MEs. When removing multi-allelic MEs, this script keeps one with highest AF, and discards the other MEs.
- This script can take gzip-ed VCF files as inputs.

Outputs:
This script outputs four files below:
- cohort_name_MEI_biallelic.vcf.gz        : This contains biallelic MEIs which passed the filter.
- cohort_name_MEA_biallelic.vcf.gz        : This contains biallelic absent MEs which passed the filter.
- cohort_name_biallelic.vcf.gz            : This is the main output. This contains biallelic polymorphic MEs which passed the filter. This file can be used for imputation.
- cohort_name_biallelic.bed.gz            : This is a bed file which contains positions of MEs. SNPs overlap with the positions listed in this file should be removed from imputation (e.g. plink --exclude bed0 cohort_name_biallelic.bed.gz).
- multiallelic_ME_summary.log             : This contains summary of multi-allelic MEs.

Show help message:
python %prog -h
'''


import os,sys,glob,gzip,argparse
import collections


version='v0.1.1 2021/02/23'


parser=argparse.ArgumentParser(description='')
parser.add_argument('-i', metavar='str', type=str, help='Required. Specify a joint-called VCF of MEIs, which must be generated by the "joint_calling" pipeline of MEGAnE.')
parser.add_argument('-a', metavar='str', type=str, help='Required. Specify a joint-called VCF of absent MEs, which must be generated by the "joint_calling" pipeline of MEGAnE.')
parser.add_argument('-cohort_name', metavar='str', type=str, help='Optional. Specify your cohort name, which will be used as output file names. If not specified, MEGAnE adds arbitrary name.')
parser.add_argument('-outdir', metavar='str', type=str, help='Optional. Specify output directory. Default: ./vcf_for_impute_out', default='./vcf_for_impute_out')
parser.add_argument('-do_not_overwrite', help='Optional. Specify if you do NOT overwrite previous results.', action='store_true')
parser.add_argument('-v', '--version', action='version', version='MEGAnE %s %s' % (os.path.basename(__file__), version))
args=parser.parse_args()
args.version=version


# start
import init
init.init_reshape_vcf(args, version)


# logging
import log
args.logfilename='multiallelic_ME_summary.log'
if os.path.exists(os.path.join(args.outdir, args.logfilename)) is True:
    os.remove(os.path.join(args.outdir, args.logfilename))
log.start_log(args)
log.logger.debug('Logging started.')


# initial check
import initial_check
log.logger.debug('This is %s version %s' % (__file__, version))
print()
log.logger.info('Initial check started.')
initial_check.check_reshape_vcf(args, sys.argv)


ins=args.i
abs=args.a
cohort=args.cohort_name


# main
import reshape_vcf_for_impute
ins_nonoverlap=reshape_vcf_for_impute.resolve_overlap_in_a_vcf(ins, os.path.join(args.outdir, '%s_MEI' % cohort))
abs_nonoverlap=reshape_vcf_for_impute.resolve_overlap_in_a_vcf(abs, os.path.join(args.outdir, '%s_MEA' % cohort))
final_outf=reshape_vcf_for_impute.resolve_overlap_between_vcf_vcf(ins_nonoverlap, abs_nonoverlap, os.path.join(args.outdir, cohort))
reshape_vcf_for_impute.convert_to_bed(final_outf)
log.logger.info('\n\nMulti-allelic ME removal finished. Please see: %s\n' % final_outf)


