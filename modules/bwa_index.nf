process BWA_INDEX {

    tag "H37Rv"

    input:
    path reference

    output:
    tuple path("H37Rv.fasta"), path("H37Rv.fasta.*"), emit: indexed_reference

    script:
    """
    bwa index H37Rv.fasta
    samtools faidx H37Rv.fasta
    """
}
