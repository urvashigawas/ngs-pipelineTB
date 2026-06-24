nextflow.enable.dsl = 2

include { FASTQC }        from './modules/fastqc'
include { BWA_INDEX }     from './modules/bwa_index'
include { BWA_MEM }       from './modules/bwa_mem'
include { SAMTOOLS_SORT } from './modules/samtools_sort'
include { SAMTOOLS_INDEX } from './modules/samtools_index'
include { BCFTOOLS_CALL } from './modules/bcftools_call'
include { FILTER_VARIANTS } from './modules/filter_variants'

workflow {

    reads_ch = Channel.fromPath(params.reads)
    ref_ch   = Channel.fromPath(params.reference)

    FASTQC(reads_ch)

    indexed_ref = BWA_INDEX(ref_ch)

    aligned_bam = BWA_MEM(reads_ch, indexed_ref)

    sorted_bam  = SAMTOOLS_SORT(aligned_bam)

    indexed_bam = SAMTOOLS_INDEX(sorted_bam)

    raw_vcf     = BCFTOOLS_CALL(sorted_bam, indexed_ref)

    FILTER_VARIANTS(raw_vcf)
}
