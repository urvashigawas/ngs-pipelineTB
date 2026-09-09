process TB_PROFILER {

    tag "${reads.simpleName}"

    publishDir "${params.outdir}/tbprofiler", mode: "copy"

    input:
    path reads

    output:
    path "tbprofiler.results.json"
    path "tbprofiler.results.txt"
    path "tbprofiler.results.csv"

    script:
    """
    tb-profiler profile \
        -1 ${reads} \
        --txt \
        --csv

    cp results/tbprofiler.results.json tbprofiler.results.json
    cp results/tbprofiler.results.txt tbprofiler.results.txt
    cp results/tbprofiler.results.csv tbprofiler.results.csv
    """
}
