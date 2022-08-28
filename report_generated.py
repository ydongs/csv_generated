import csv

auto_file = open('summary_auto_channels_last_jit.log', 'r')
manual_file = open('summary_manual_channels_last_jit.log', 'r')
wo_file = open('summary_without_channels_last_jit.log', 'r')


def generated_report(auto, manual, wo):
    with open('fp32_inference_perf_report.csv', 'r+', newline='') as report_generated:
        writer = csv.writer(report_generated)
        writer.writerow(
            ['model', 'auto_jit', 'manual_jit', 'without_jit', 'auto_vs_wo_speedup', 'auto_vs_manual_%diff'])
        model = []
        auto_jit = []
        manual_jit = []
        without_jit = []
        for line in auto:
            line = line.split()
            model.append(line[1])
            auto_jit.append(line[5])

        for line in manual:
            line = line.split()
            manual_jit.append(line[5])

        for line in wo:
            line = line.split()
            without_jit.append(line[5])

        for i in range(len(model)):
            auto_vs_wo_speedup = '%.6f' % (float(auto_jit[i]) / float(without_jit[i]))
            auto_vs_manual_diff = '%.6f' % abs((float(manual_jit[i]) - float(without_jit[i])) / float(without_jit[i]))
            lists = [model[i], auto_jit[i], manual_jit[i], without_jit[i], auto_vs_wo_speedup, auto_vs_manual_diff]
            writer.writerows([lists])


generated_report(auto_file, manual_file, wo_file)
