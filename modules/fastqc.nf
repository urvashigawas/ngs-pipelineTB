process FASTQC {

    tag "$reads.simpleName"

    publishDir "${params.outdir}/fastqc", mode: 'copy'

    input:
    path reads

    output:
    path "*_fastqc.html"
    path "*_fastqc.zip"

    script:
    """
    fastqc \
        --threads ${task.cpus} \
        ${reads}
    """
}
