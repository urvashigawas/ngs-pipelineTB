import json
import csv
import gzip
import sys


def load_bcftools_variants(vcf_file):
    variants = {}

    with gzip.open(vcf_file, "rt") as f:
        for line in f:
            if line.startswith("#"):
                continue

            fields = line.rstrip("\n").split("\t")

            chrom = fields[0]
            pos = int(fields[1])
            ref = fields[3]
            alt = fields[4]
            qual = fields[5]
            filt = fields[6]
            info = fields[7]
            sample = fields[9]

            info_dict = {}

            for item in info.split(";"):
                if "=" in item:
                    key, value = item.split("=", 1)
                    info_dict[key] = value

            format_keys = fields[8].split(":")
            sample_values = sample.split(":")
            sample_dict = dict(zip(format_keys, sample_values))

            variants[(chrom, pos, ref, alt)] = {
                "DP": info_dict.get("DP", ""),
                "MQ": info_dict.get("MQ", ""),
                "QUAL": qual,
                "FILTER": filt,
                "GT": sample_dict.get("GT", ""),
            }

    return variants


def get_drugs(variant):
    return sorted({
        d.get("drug", "")
        for d in variant.get("drugs", [])
        if d.get("drug")
    })


def get_confidence(variant):
    return ";".join(sorted({
        a.get("confidence", "")
        for a in variant.get("annotation", [])
        if a.get("confidence")
    }))


def main():

    if len(sys.argv) != 4:
        sys.exit(
            "Usage: python compare_variants.py "
            "<tbprofiler.json> <filtered.vcf.gz> <output.tsv>"
        )

    tbprofiler_json = sys.argv[1]
    bcftools_vcf = sys.argv[2]
    output = sys.argv[3]

    with open(tbprofiler_json) as f:
        data = json.load(f)

    tb_variants = data["dr_variants"]
    bcftools_variants = load_bcftools_variants(bcftools_vcf)

    columns = [
        "CHROM",
        "POS",
        "REF",
        "ALT",
        "GENE",
        "LOCUS_TAG",
        "TBPROFILER_CHANGE",
        "DRUGS",
        "CONFIDENCE",
        "TBPROFILER_DEPTH",
        "TBPROFILER_FREQ",
        "BCFTOOLS_STATUS",
        "BCFTOOLS_DP",
        "BCFTOOLS_MQ",
        "BCFTOOLS_QUAL",
        "BCFTOOLS_FILTER",
        "BCFTOOLS_GT",
    ]

    with open(output, "w", newline="") as out:

        writer = csv.DictWriter(
            out,
            fieldnames=columns,
            delimiter="\t"
        )

        writer.writeheader()

        for variant in tb_variants:

            chrom = "NC_000962.3"
            pos = variant["pos"]
            ref = variant["ref"]
            alt = variant["alt"]

            key = (chrom, pos, ref, alt)

            if key in bcftools_variants:
                bcf = bcftools_variants[key]
                status = "MATCH"
            else:
                bcf = {
                    "DP": "",
                    "MQ": "",
                    "QUAL": "",
                    "FILTER": "",
                    "GT": "",
                }
                status = "NOT_FOUND"

            writer.writerow({
                "CHROM": chrom,
                "POS": pos,
                "REF": ref,
                "ALT": alt,
                "GENE": variant.get("gene_name", ""),
                "LOCUS_TAG": variant.get("locus_tag", ""),
                "TBPROFILER_CHANGE": variant.get("change", ""),
                "DRUGS": ";".join(get_drugs(variant)),
                "CONFIDENCE": get_confidence(variant),
                "TBPROFILER_DEPTH": variant.get("depth", ""),
                "TBPROFILER_FREQ": variant.get("freq", ""),
                "BCFTOOLS_STATUS": status,
                "BCFTOOLS_DP": bcf["DP"],
                "BCFTOOLS_MQ": bcf["MQ"],
                "BCFTOOLS_QUAL": bcf["QUAL"],
                "BCFTOOLS_FILTER": bcf["FILTER"],
                "BCFTOOLS_GT": bcf["GT"],
            })

    print(f"Compared {len(tb_variants)} TB-Profiler resistance variants")
    print(f"Found {len(bcftools_variants)} BCFtools variants")
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
