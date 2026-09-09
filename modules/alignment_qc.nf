process ALIGNMENT_QC {

    tag "${bam.simpleName}"

    publishDir "${params.outdir}/qc", mode: "copy"

    input:
    path bam
    path qc_script

    output:
    path "alignment_qc.tsv"

    script:
    """
    samtools flagstat ${bam} > flagstat.txt
    samtools depth ${bam} > depth.txt

    python ${qc_script} \
        flagstat.txt \
        depth.txt \
        alignment_qc.tsv
    """
}
