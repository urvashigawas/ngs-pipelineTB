process FILTER_VARIANTS {

    publishDir "${params.outdir}/filtered", mode: "copy"

    input:
    path vcf

    output:
    path "filtered.vcf"

    script:
    """
    bcftools filter -i 'QUAL>20' ${vcf} -o filtered.vcf
    """
}
