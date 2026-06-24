nextflow.enable.dsl = 2

include { FASTQC } from './modules/fastqc'

workflow {

    reads_ch = Channel.fromPath(params.reads)

    FASTQC(reads_ch)
}
