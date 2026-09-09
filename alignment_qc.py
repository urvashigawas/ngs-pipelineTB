import sys
import statistics


flagstat_file = sys.argv[1]
depth_file = sys.argv[2]
output_file = sys.argv[3]


with open(flagstat_file) as f:
    lines = f.readlines()


def get_count(pattern):
    for line in lines:
        if pattern in line:
            return int(line.split("+")[0].strip().split()[0])
    return 0


total_reads = get_count("in total")
mapped_reads = get_count("mapped (")

mapping_percent = (
    mapped_reads / total_reads * 100
    if total_reads else 0
)


depths = []

with open(depth_file) as f:
    for line in f:
        fields = line.rstrip().split("\t")
        if len(fields) >= 3:
            depths.append(int(fields[2]))


if depths:
    mean_depth = statistics.mean(depths)
    median_depth = statistics.median(depths)
    covered_bases = sum(d > 0 for d in depths)
    total_positions = len(depths)
    genome_coverage = covered_bases / total_positions * 100
else:
    mean_depth = 0
    median_depth = 0
    genome_coverage = 0


with open(output_file, "w") as out:
    out.write(
        "TOTAL_READS\tMAPPED_READS\tMAPPING_PERCENT\t"
        "MEAN_DEPTH\tMEDIAN_DEPTH\tGENOME_COVERAGE_PERCENT\n"
    )

    out.write(
        f"{total_reads}\t"
        f"{mapped_reads}\t"
        f"{mapping_percent:.2f}\t"
        f"{mean_depth:.2f}\t"
        f"{median_depth:.2f}\t"
        f"{genome_coverage:.2f}\n"
    )
