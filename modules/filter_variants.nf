process FILTER_VARIANTS {

    publishDir "${params.outdir}/filtered", mode: "copy"

    input:
    path vcf

    output:
    path "filtered.vcf.gz"
    path "filtered.vcf.gz.csi"

    script:
    """
    bcftools filter \
        -i 'DP>=10 && MQ>=30 && QUAL>=30' \
        ${vcf} \
        -Oz \
        -o filtered.vcf.gz

    bcftools index filtered.vcf.gz
    """
}
