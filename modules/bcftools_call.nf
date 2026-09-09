process BCFTOOLS_CALL {

    tag "${bam.simpleName}"

    publishDir "${params.outdir}/variants", mode: "copy"

    input:
    path bam
    tuple path(reference), path(index_files)

    output:
    path "variants.vcf.gz", emit: vcf
    path "variants.vcf.gz.csi", emit: vcf_index

    script:
    """
    bcftools mpileup \
        -f ${reference} \
        ${bam} | \
    bcftools call \
        -mv \
        --ploidy 1 \
        -Oz \
        -o variants.vcf.gz

    bcftools index variants.vcf.gz

    bcftools view -h variants.vcf.gz | \
        sed 's/ID=MQ,Number=1,Type=Integer/ID=MQ,Number=1,Type=Float/' \
        > fixed_header.txt

    bcftools reheader \
        -h fixed_header.txt \
        -o variants.fixed.vcf.gz \
        variants.vcf.gz

    mv variants.fixed.vcf.gz variants.vcf.gz

    bcftools index -f variants.vcf.gz
    """
}
