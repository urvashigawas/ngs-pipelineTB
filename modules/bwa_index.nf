process BWA_INDEX {

    tag "BWA index"

    input:
    path reference

    output:
    tuple path("reference.fasta"), path("reference.fasta.*"), emit: indexed_reference

    script:
    """
    cp ${reference} reference.fasta
    bwa index reference.fasta
    """
}
