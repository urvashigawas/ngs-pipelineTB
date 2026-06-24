process BWA_MEM {

    tag "${reads.simpleName}"

    publishDir "${params.outdir}/alignment", mode: "copy"

    input:
    path reads
    path refdir

    output:
    path "${reads.simpleName}.sam"

    script:
    """
    bwa mem \
        -t ${task.cpus} \
        H37Rv/H37Rv.fasta \
        ${reads} \
        > ${reads.simpleName}.sam
    """
}
