# ngs-pipelineTB

A modular **Nextflow DSL2** pipeline for reference-based variant analysis of *Mycobacterium tuberculosis* whole-genome sequencing (WGS) data.

The pipeline performs sequencing quality control, reference indexing, read alignment, BAM processing, alignment quality assessment, variant calling and filtering. It additionally runs **TB-Profiler** for tuberculosis drug-resistance interpretation and performs an explicit **TB-Profiler–BCFtools concordance analysis**.

The workflow was developed and validated using a real *M. tuberculosis* WGS dataset on C-DAC iceCloud.

---

## Overview

| Component           | Details                        |
| ------------------- | ------------------------------ |
| Organism            | *Mycobacterium tuberculosis*   |
| Reference           | H37Rv / NC_000962.3            |
| Reference size      | ~4.41 Mb                       |
| Workflow engine     | Nextflow DSL2                  |
| Read QC             | FastQC                         |
| Alignment           | BWA-MEM                        |
| BAM processing      | SAMtools                       |
| Variant calling     | BCFtools                       |
| Variant filtering   | BCFtools-based filtering       |
| Resistance analysis | TB-Profiler                    |
| Alignment QC        | SAMtools + Python              |
| Concordance         | TB-Profiler vs BCFtools        |
| Execution           | Local / HPC / Cloud compatible |

---

## Workflow

```text
                         Raw FASTQ
                             │
                             ▼
                    ┌─────────────────┐
                    │     FastQC      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   BWA Index     │
                    │     H37Rv      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │    BWA-MEM      │
                    │ Read Alignment  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ SAMtools Sort   │
                    └────────┬────────┘
                             │
                    ┌────────┴────────┐
                    ▼                 ▼
           ┌────────────────┐  ┌─────────────────┐
           │ Alignment QC   │  │ SAMtools Index  │
           │ flagstat/depth │  │      BAM        │
           └────────────────┘  └────────┬────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ BCFtools Call   │
                               └────────┬────────┘
                                        │
                                        ▼
                               ┌─────────────────┐
                               │ Variant Filter  │
                               └────────┬────────┘
                                        │
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
                ┌─────────────────┐          ┌─────────────────┐
                │   Filtered VCF  │          │   TB-Profiler   │
                └────────┬────────┘          └────────┬────────┘
                         │                            │
                         └──────────────┬─────────────┘
                                        ▼
                            ┌───────────────────────┐
                            │ TB-Profiler / BCFtools│
                            │      Concordance      │
                            └───────────────────────┘
```

---

## Pipeline Components

### 1. FastQC

FastQC is used for initial sequencing-read quality control.

The process generates standard FastQC HTML and ZIP reports.

### 2. BWA Index

The H37Rv reference genome is indexed using BWA before read alignment.

### 3. BWA-MEM

Sequencing reads are aligned against the H37Rv reference genome using BWA-MEM.

### 4. SAMtools Sort

The alignment output is coordinate-sorted to generate a sorted BAM file.

### 5. Alignment QC

Alignment and coverage statistics are generated using:

* `samtools flagstat`
* `samtools depth`

The accompanying `alignment_qc.py` script calculates:

* Total reads
* Mapped reads
* Mapping percentage
* Mean depth
* Median depth
* Genome coverage percentage

### 6. SAMtools Index

The sorted BAM file is indexed using `samtools index`.

### 7. BCFtools Variant Calling

Variants are called from the sorted BAM against the H37Rv reference using BCFtools.

### 8. Variant Filtering

The raw BCFtools variant calls are filtered to generate a higher-confidence variant set.

### 9. TB-Profiler

TB-Profiler is run independently on the sequencing reads.

It provides:

* MTB lineage information
* Drug-resistance-associated variants
* Resistance-associated drugs
* Variant depth and frequency
* Resistance confidence information
* QC metrics

TB-Profiler is used as an independent resistance interpretation component rather than replacing the BCFtools variant-calling workflow.

### 10. TB-Profiler / BCFtools Concordance

The pipeline compares TB-Profiler resistance-associated variants with the filtered BCFtools VCF.

The comparison records:

* Chromosome
* Position
* Reference allele
* Alternate allele
* Gene
* Mutation
* Associated drugs
* TB-Profiler confidence
* TB-Profiler depth
* TB-Profiler allele frequency
* BCFtools depth
* Mapping quality
* Variant quality
* FILTER status
* Genotype
* Concordance status

This provides an independent variant-level comparison between the resistance interpretation and the underlying variant-calling workflow.

---

## Example Dataset

The real-data validation used:

```text
SRA accession: ERR3275683
BioProject:    PRJEB32037
```

The sequencing data were aligned against:

```text
Reference: H37Rv
Accession: NC_000962.3
Size:      ~4.41 Mb
```

The FASTQ file used during validation was:

```text
data/ERR3275683.fastq.gz
```

---

## Validated Results

The complete Nextflow workflow was successfully executed on the real WGS dataset.

### Alignment and Coverage QC

| Metric          |    Result |
| --------------- | --------: |
| Total reads     | 3,703,089 |
| Mapped reads    | 3,700,170 |
| Mapping rate    |    99.92% |
| Mean depth      |   100.05× |
| Median depth    |       98× |
| Genome coverage |   100.00% |

These results indicate high alignment rate and approximately 100× sequencing depth across the H37Rv reference for the validated dataset.

### BCFtools Variant Calling

The validated workflow produced:

```text
Raw variants:       965
Filtered variants:  873
```

### TB-Profiler

The validated TB-Profiler run reported:

```text
Resistance profile: HR-TB
Lineage:            lineage4.5
Median depth:       100×
```

One resistance-associated variant was reported:

```text
Gene:        inhA
Mutation:    c.-777C>T
Position:    NC_000962.3:1673425
Reference:   C
Alternate:   T
Depth:       96
Frequency:   1.0
Confidence:  Assoc w R
```

The variant was associated with:

```text
Isoniazid
Ethionamide
Prothionamide
```

### TB-Profiler / BCFtools Concordance

The same variant was identified in the filtered BCFtools VCF:

```text
Position:    NC_000962.3:1673425
Reference:   C
Alternate:   T
BCFtools DP: 105
MQ:          60
QUAL:        225.417
FILTER:      PASS
GT:          1
```

The concordance analysis classified the variant as:

```text
MATCH
```

This demonstrates agreement between the TB-Profiler resistance-associated variant and the independent BCFtools filtered variant call for this validated dataset.

---

## Project Structure

```text
ngs-pipelineTB/
│
├── main.nf
├── nextflow.config
├── README.md
├── .gitignore
│
├── modules/
│   ├── fastqc.nf
│   ├── bwa_index.nf
│   ├── bwa_mem.nf
│   ├── samtools_sort.nf
│   ├── samtools_index.nf
│   ├── alignment_qc.nf
│   ├── bcftools_call.nf
│   ├── filter_variants.nf
│   ├── tb_profiler.nf
│   └── variant_comparison.nf
│
├── alignment_qc.py
├── compare_variants.py
│
├── data/
│   └── ERR3275683.fastq.gz
│
└── reference/
    └── H37Rv.fasta
```

Generated sequencing data, alignment files, variant files, reference indexes, Nextflow work directories, and pipeline results are excluded from version control according to the repository's `.gitignore` configuration.

---

## Computing Environment

The real-data pipeline was developed and executed on **C-DAC iceCloud** using a Jupyter Notebook terminal as the working interface.

The pipeline itself is not dependent on iceCloud and can be executed on other Linux-based environments, including:

* Local systems
* HPC clusters
* Cloud compute instances

The current configuration uses the local Nextflow executor.

---

## Requirements

The current pipeline requires:

* Linux/Unix environment
* Java
* Nextflow
* Python 3
* FastQC
* BWA
* SAMtools
* BCFtools
* TB-Profiler

The pipeline can be adapted to Conda, containerized, HPC, or cloud execution environments.

### Example Conda Environment

```bash
conda create -n ngs-pipelineTB \
    -c conda-forge \
    -c bioconda \
    bwa samtools bcftools fastqc nextflow python
```

Activate the environment:

```bash
conda activate ngs-pipelineTB
```

TB-Profiler should be installed separately according to its installation requirements.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/urvashigawas/ngs-pipelineTB.git
cd ngs-pipelineTB
```

Verify Nextflow:

```bash
nextflow -version
```

---

## Usage

### Run with FASTQ files

The default configuration expects:

```text
data/*.fastq.gz
```

Run the pipeline using:

```bash
nextflow run main.nf \
    --reads "data/*.fastq.gz" \
    --reference reference/H37Rv.fasta \
    --outdir results
```

A specific FASTQ file can also be supplied:

```bash
nextflow run main.nf \
    --reads "data/ERR3275683.fastq.gz" \
    --reference reference/H37Rv.fasta \
    --outdir results
```

### Resume a Previous Run

Nextflow caching can be used to resume a previous execution:

```bash
nextflow run main.nf -resume
```

---

## Parameters

The current `nextflow.config` defines:

| Parameter     | Description                | Default                 |
| ------------- | -------------------------- | ----------------------- |
| `--reads`     | Input FASTQ file pattern   | `data/*.fastq.gz`       |
| `--reference` | H37Rv reference FASTA      | `reference/H37Rv.fasta` |
| `--outdir`    | Output directory           | `results`               |
| `--cpus`      | Default CPU allocation     | `4`                     |
| `--memory`    | Default memory allocation  | `8 GB`                  |
| `--time`      | Default process time limit | `2h`                    |

Individual processes have their own resource overrides where required.

For example:

* FastQC: 2 CPUs, 2 GB memory, 1 hour
* BWA index: 4 CPUs, 8 GB memory, 2 hours
* BWA-MEM: 4 CPUs, 8 GB memory, 3 hours
* SAMtools index: 2 CPUs, 4 GB memory

---

## Output Structure

The pipeline publishes results into the configured output directory.

```text
results/
│
├── fastqc/
│   ├── *_fastqc.html
│   └── *_fastqc.zip
│
├── alignment/
│   └── alignment outputs
│
├── bam/
│   ├── *.sorted.bam
│   └── *.sorted.bam.bai
│
├── qc/
│   └── alignment_qc.tsv
│
├── variants/
│   └── BCFtools variant output
│
├── filtered/
│   └── filtered VCF
│
├── tbprofiler/
│   └── TB-Profiler results
│
└── comparison/
    └── tbprofiler_bcftools_comparison.tsv
```

The exact filenames depend on the input sample and process configuration.

---

## Alignment QC Output

The alignment QC process generates:

```text
results/qc/alignment_qc.tsv
```

The report contains:

```text
TOTAL_READS
MAPPED_READS
MAPPING_PERCENT
MEAN_DEPTH
MEDIAN_DEPTH
GENOME_COVERAGE_PERCENT
```

Example from the validated dataset:

```text
TOTAL_READS  MAPPED_READS  MAPPING_PERCENT  MEAN_DEPTH  MEDIAN_DEPTH  GENOME_COVERAGE_PERCENT
3703089      3700170       99.92             100.05      98.00         100.00
```

---

## Variant Concordance Output

The concordance process generates:

```text
results/comparison/tbprofiler_bcftools_comparison.tsv
```

The output allows resistance-associated variants identified by TB-Profiler to be checked against the filtered BCFtools VCF.

Example validated record:

```text
NC_000962.3  1673425  C  T  inhA  Rv1484  c.-777C>T  ethionamide;isoniazid;prothionamide  Assoc w R  96  1.0  MATCH  105  60  225.417  PASS  1
```

---

## Reproducibility

The workflow uses Nextflow DSL2 and Nextflow's process-level caching.

Reproducibility is supported through:

* Modular Nextflow processes
* Explicit process inputs and outputs
* Version-controlled workflow code
* Configurable computational resources
* Nextflow caching
* `-resume` support
* Separate automated testing infrastructure

The workflow can be extended with additional analysis modules without restructuring the complete pipeline.

---

## CI/CD Demonstration

A separate branch named `ci-cd-upgrade` was developed to demonstrate **GitHub Actions-based CI/CD testing**.

The CI/CD implementation uses a **small test dataset** rather than the large real WGS dataset used for scientific validation.

This separation is intentional:

```text
main
│
└── Real-data pipeline validation
    └── ERR3275683

ci-cd-upgrade
│
└── Lightweight CI/CD testing
    ├── Small test FASTQ
    ├── Small H37Rv test reference
    └── GitHub Actions workflow
```

The CI workflow performs tasks such as:

1. Checking out the repository
2. Setting up Java
3. Installing Nextflow
4. Installing required bioinformatics tools
5. Running the pipeline using test data
6. Checking expected output files

The CI/CD branch contains:

```text
.github/workflows/ci.yml
assets/test/ref_h37rv.fasta
assets/test/sample.fastq.gz
```

The purpose of this branch is to demonstrate automated pipeline testing and regression-checking using a lightweight dataset. It is **not intended to replace full-scale validation using real WGS data**.

---

## Development and Validation

The project was developed incrementally, with individual processes tested before integration into the complete workflow.

The current pipeline includes:

* Modular DSL2 architecture
* Reference-based MTB alignment
* Alignment QC
* BCFtools variant calling
* Variant filtering
* TB-Profiler resistance interpretation
* TB-Profiler / BCFtools concordance
* Nextflow resume support
* Resource configuration
* Separate CI/CD test infrastructure

The complete real-data workflow was successfully executed using the `ERR3275683` dataset.

---

## Limitations

This repository represents a **research and bioinformatics workflow**, not a validated clinical diagnostic system.

Important considerations include:

* Filtering parameters may need adjustment for different sequencing datasets.
* TB-Profiler results depend on the version and underlying resistance database.
* The example validation uses one MTB WGS dataset.
* The reported QC and variant results should not be generalized to all MTB sequencing datasets.
* Clinical or public-health interpretation requires appropriate validated procedures and current reference resources.
* The CI/CD workflow uses a small test dataset and is intended for software/regression testing rather than full-scale WGS validation.

---

## Dataset Citation

The real-data validation used:

```text
SRA accession: ERR3275683
BioProject:    PRJEB32037
```

Users should cite the original study associated with the sequencing dataset when using this example dataset.

Software and database citations should also be provided for tools used in downstream analyses, including Nextflow, FastQC, BWA, SAMtools, BCFtools, and TB-Profiler.

---

## Contributing

Issues, bug reports, and pull requests are welcome.

Potential future improvements include:

* Containerized execution
* Expanded CI/CD regression testing
* Multi-sample support
* Additional alignment and variant QC
* Expanded resistance concordance analysis
* HPC execution profiles
* Cloud execution profiles
* Automated software-version reporting

---

## License

Please refer to the repository license for the terms governing this project.

Individual software tools and databases used by the pipeline are subject to their respective licenses and terms of use.
