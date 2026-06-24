# ngs-pipelineTB

A **Nextflow DSL2** pipeline for reference-based variant calling in *Mycobacterium tuberculosis* whole-genome sequencing (WGS) data. It performs quality control, alignment, sorting, and variant calling, producing a filtered VCF that can be screened for clinically relevant drug-resistance mutations.

---

## Overview

| | |
|---|---|
| **Organism** | *Mycobacterium tuberculosis* |
| **Reference genome** | H37Rv (NC_000962.3, ~4.41 Mb) |
| **Workflow engine** | Nextflow (DSL2) |
| **Core tools** | FastQC, BWA, SAMtools, BCFtools |
| **Input** | Illumina paired/single-end FASTQ or SRA accession |
| **Output** | Sorted BAM, filtered VCF, QC reports |

This pipeline is built to mirror a real clinical genomics workflow: align WGS reads to the H37Rv reference, call variants, and compare results against known drug-resistance loci (e.g. `rpoB`, `katG`, `embB`, `pncA`).

---

## Computing Environment

This pipeline was developed and executed on **C-DAC's iceCloud** computing platform, using a **Jupyter Notebook terminal** as the working interface for running shell commands, Nextflow, and bioinformatics tools.

- **Platform:** C-DAC iceCloud (remote cloud compute instance)
- **Interface:** Jupyter Notebook terminal (browser-based shell access)
- **Execution:** All commands — environment setup, tool installation, and pipeline runs — were carried out directly in the Jupyter terminal rather than a local laptop terminal

The pipeline itself has no hard dependency on this environment — it can equally be run on a local machine, a different HPC/cloud instance, or any system with Nextflow and the required tools installed.

---

## Workflow


```

```
          Raw FASTQ
              │
              ▼
     Quality Control (FastQC)
              │
              ▼
     Reference Genome (H37Rv)
              │
              ▼
          BWA Index
              │
              ▼
      Read Alignment (BWA-MEM)
              │
              ▼
    SAMtools Sort + Index (BAM)
              │
              ▼
    Variant Calling (BCFtools)
              │
              ▼
      Variant Filtering
              │
              ▼
      Final Filtered VCF

```

```

---

## Features

- DSL2 modular structure (`modules/`) — each step is an isolated, reusable process
- Works with local FASTQ files **or** a public SRA accession
- Configurable parameters (threads, memory, minimum depth, etc.)
- Resume support via Nextflow's built-in caching (`-resume`)
- Lightweight enough to run on a laptop, HPC node, or cloud instance — small bacterial genome, fast turnaround
- Developed and tested on C-DAC's iCloud platform via a Jupyter terminal

---

## Requirements

- [Nextflow](https://www.nextflow.io/) ≥ 22.10
- Java 11+
- One of: Conda/Mamba, or Docker/Singularity (for containerized execution)
- Tools used by the pipeline: `bwa`, `samtools`, `bcftools`, `fastqc`

> These were installed and run inside a **Jupyter terminal session on C-DAC's iCloud**. The same setup works in any standard Linux shell (local, HPC, or cloud).

Install the core tools via Conda (run inside the Jupyter terminal):

```bash
conda create -n ngs-pipelineTB -c bioconda -c conda-forge \
    bwa samtools bcftools fastqc
conda activate ngs-pipelineTB

```

---

## Installation

Run inside a Jupyter terminal (or any shell):

```bash
git clone [https://github.com/](https://github.com/)<your-username>/ngs-pipelineTB.git
cd ngs-pipelineTB

```

---

## Usage

### Run with local FASTQ files

```bash
nextflow run main.nf \
    --reads "data/*_R{1,2}.fastq.gz" \
    --reference reference/H37Rv.fasta \
    --outdir results

```

### Run with a public SRA accession

```bash
nextflow run main.nf \
    --sra ERR3275683 \
    --reference reference/H37Rv.fasta \
    --outdir results

```

### Resume a previous run

```bash
nextflow run main.nf -resume

```

---

## Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `--reads` | Glob pattern for input FASTQ files | — |
| `--sra` | SRA run accession to download and use as input | — |
| `--reference` | Path to reference genome FASTA | `reference/H37Rv.fasta` |
| `--outdir` | Output directory | `results` |
| `--threads` | Threads per process | `4` |
| `--min_depth` | Minimum depth for variant filtering | `10` |

> Adjust this table to match the parameters actually defined in `nextflow.config` / `main.nf`.

---

## Output

```
results/
├── fastqc/            # Read quality reports (.html)
├── alignment/         # Sorted and indexed BAM files
└── variants/          # Final filtered VCF files containing high-confidence variants

```

### Key Findings & Pipeline Metrics

* **Variant Classification:** Successfully filtered down background mutations to isolate **High** and **Moderate** impact variants, identifying major non-synonymous amino acid substitutions (e.g., missense mutations) alongside severe structural alterations (e.g., frameshifts in `Rv0026` and `ctpI`, nonsense truncation in `Rv0197`).
* **Drug Resistance Profile:**
* **Fluoroquinolones:** Detected classical mutations in the DNA Gyrase Subunit A (`gyrA`) gene, including `p.Ser95Thr`, `p.Glu21Gln`, and `p.Gly668Asp`.
* **Isoniazid:** Identified a `p.Lys198Asn` mutation in `fabG1`, a key locus implicated in clinical co-resistance phenotypes.


* **Cell Wall Dynamics:** Isolated structural changes in virulence and cell-wall integrity paths, including a `p.Pro631del` deletion in the Penicillin-Binding Protein (`ponA1`) and multiple alterations across hyper-variable immune-evasion gene families (`PE/PPE`).
* **Quality Benchmarks:** The run yielded an overall transition-to-transversion (Ts/Tv) ratio of **1.69**, with variants overwhelmingly fixed at 100% allele frequency and maintaining a high average sequencing quality score of **197.52**.

---

## Project Structure

```
ngs-pipelineTB/
├── main.nf              # Pipeline entry point
├── nextflow.config       # Default parameters & execution profiles
├── modules/             # DSL2 process modules (QC, alignment, variant calling, etc.)
├── results/
├── .gitignore        
└── README.md

```

---

## Roadmap

* [ ] Variant annotation with SnpEff
* [ ] MultiQC summary report
* [ ] Dockerfile / Conda environment file for full reproducibility
* [ ] GitHub Actions CI for automated testing
* [ ] Automatic reference + SRA download helper script

---

## Citation

If you use this pipeline with the example dataset, please cite the original study associated with SRA accession **ERR3275683** (BioProject PRJEB32037) on NCBI.

---

## Contributing

Issues and pull requests are welcome. If you spot a bug or have an improvement in mind, feel free to open an issue.

```
