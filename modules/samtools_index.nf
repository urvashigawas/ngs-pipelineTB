process SAMTOOLS_INDEX {

    input:
    path bam

    output:
    path "*.bai"

    script:
    """
    samtools index ${bam}
    """
}
