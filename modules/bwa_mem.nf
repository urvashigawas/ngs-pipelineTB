process BWA_MEM {

    tag "${reads.simpleName}"

    publishDir "${params.outdir}/alignment", mode: "copy"

    input:
    path reads
    tuple path(reference), path(index_files)

    output:
    path "${reads.simpleName}.sam"

    script:
    """
    bwa mem \
        -t ${task.cpus} \
        ${reference} \
        ${reads} \
        > ${reads.simpleName}.sam
    """
}
