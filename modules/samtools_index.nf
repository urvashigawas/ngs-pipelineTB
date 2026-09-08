process SAMTOOLS_INDEX {

    tag "${bam.simpleName}"

    publishDir "${params.outdir}/bam", mode: "copy"

    input:
    path bam

    output:
    path "*.bai"

    script:
    """
    samtools index ${bam}
    """
}
