process BCFTOOLS_CALL {

    publishDir "${params.outdir}/variants", mode: "copy"

    input:
    path bam
    path refdir

    output:
    path "variants.vcf.gz"

    script:
    """
    bcftools mpileup -f H37Rv/H37Rv.fasta ${bam} | \
    bcftools call -mv -Oz -o variants.vcf.gz
    """
}
