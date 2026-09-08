process BCFTOOLS_CALL {

    publishDir "${params.outdir}/variants", mode: "copy"

    input:
    path bam
    tuple path(reference), path(index_files)

    output:
    path "variants.vcf.gz"

    script:
    """
    bcftools mpileup \
        -f ${reference} \
        ${bam} | \
    bcftools call \
        -mv \
        -Oz \
        -o variants.vcf.gz
    """
}
