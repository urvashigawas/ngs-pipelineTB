process SAMTOOLS_SORT {

    tag "${bam.simpleName}"

    publishDir "${params.outdir}/bam", mode: "copy"

    input:
    path bam

    output:
    path "*.bam", emit: bam

    script:
    """
    samtools sort -o ${bam.simpleName}.sorted.bam ${bam}
    """
}
