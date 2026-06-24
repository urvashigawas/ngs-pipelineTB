process BWA_INDEX {

    tag "H37Rv"

    input:
    path refdir

    output:
    path "H37Rv"

    script:
    """
    cp -r ${refdir} H37Rv

    bwa index H37Rv/H37Rv.fasta

    """
}
