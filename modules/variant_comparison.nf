process VARIANT_COMPARISON {

    publishDir "${params.outdir}/comparison", mode: "copy"

    input:
    path tbprofiler_json
    path filtered_vcf

    output:
    path "tbprofiler_bcftools_comparison.tsv"

    script:
    """
    python ${projectDir}/compare_variants.py \
        ${tbprofiler_json} \
        ${filtered_vcf} \
        tbprofiler_bcftools_comparison.tsv
    """
}
