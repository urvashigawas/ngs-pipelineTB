#!/usr/bin/env python3
"""
interpret_resistance.py

Reads a SnpEff-annotated Mycobacterium tuberculosis VCF (must contain
an ANN= field in the INFO column) and flags variants in genes known
to confer first-line drug resistance.

Usage:
    python interpret_resistance.py sample.ann.vcf

Note:
    The "known_changes" sets below are a small, well-established subset
    of high-confidence resistance mutations for quick screening. They are
    NOT exhaustive. For a complete, authoritative list, cross-check hits
    against the WHO Catalogue of Mutations in M. tuberculosis Associated
    with Drug Resistance (2nd ed., 2023) or a tool like TB-Profiler.
"""

import sys
import re

# Gene -> drug + the most well-known high-confidence resistance changes.
# Empty set = too diverse to hardcode; any hit in that gene should be
# checked manually against the WHO catalogue.
RESISTANCE_CATALOG = {
    "rpoB": {
        "drug": "Rifampicin",
        "known_changes": {"p.Ser450Leu", "p.His445Tyr", "p.Asp435Val"},
    },
    "katG": {
        "drug": "Isoniazid",
        "known_changes": {"p.Ser315Thr"},
    },
    "inhA": {
        "drug": "Isoniazid (low-level) / Ethionamide",
        "known_changes": set(),  # key resistance variant is a promoter SNP, not coding
    },
    "embB": {
        "drug": "Ethambutol",
        "known_changes": {"p.Met306Val", "p.Met306Ile", "p.Met306Leu"},
    },
    "pncA": {
        "drug": "Pyrazinamide",
        "known_changes": set(),  # resistance mutations are highly diverse across the gene
    },
}


def parse_ann_field(info_field):
    """Extract ANN= entries from a VCF INFO field. Returns a list of '|'-delimited strings."""
    match = re.search(r"ANN=([^;]+)", info_field)
    if not match:
        return []
    return match.group(1).split(",")


def main(vcf_path):
    hits = []
    with open(vcf_path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 8:
                continue
            chrom, pos, _id, ref, alt = fields[0:5]
            info = fields[7]

            for ann in parse_ann_field(info):
                parts = ann.split("|")
                if len(parts) < 11:
                    continue
                gene = parts[3]
                hgvs_p = parts[10] or "-"

                if gene in RESISTANCE_CATALOG:
                    entry = RESISTANCE_CATALOG[gene]
                    if entry["known_changes"]:
                        is_known = hgvs_p in entry["known_changes"]
                    else:
                        is_known = None  # no hardcoded list to check against
                    hits.append({
                        "chrom": chrom,
                        "pos": pos,
                        "ref": ref,
                        "alt": alt,
                        "gene": gene,
                        "hgvs_p": hgvs_p,
                        "drug": entry["drug"],
                        "is_known": is_known,
                    })

    if not hits:
        print("No variants found in the screened resistance genes "
              "(rpoB, katG, inhA, embB, pncA).")
        return

    header = f"{'Gene':<8}{'Protein change':<20}{'Drug':<28}{'Position':<14}{'Status'}"
    print(header)
    print("-" * len(header))
    for h in hits:
        if h["is_known"] is True:
            status = "MATCHES known resistance mutation"
        elif h["is_known"] is False:
            status = "novel/uncatalogued change - check WHO catalogue"
        else:
            status = "hit in gene - check WHO catalogue (diverse resistance sites)"
        pos_str = f"{h['chrom']}:{h['pos']}"
        print(f"{h['gene']:<8}{h['hgvs_p']:<20}{h['drug']:<28}{pos_str:<14}{status}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python interpret_resistance.py sample.ann.vcf")
        sys.exit(1)
    main(sys.argv[1])
