import csv

auto_jit = open('summary_auto_channels_last_jit.log', 'r')
manual_jit = open('summary_manual_channels_last_jit.log', 'r')
wo_jit = open('summary_without_channels_last_jit.log', 'r')

auto_eager = open('summary_auto_channels_last_eager.log', 'r')
manual_eager = open('summary_manual_channels_last_eager.log', 'r')
wo_eager = open('summary_without_channels_last_eager.log', 'r')

def generated_report(auto, manual, wo, option):
    with open('fp32_inference_perf'+option+'_report.csv', 'r+', newline='') as report_generated:
        writer = csv.writer(report_generated)
        writer.writerow(
            ['model', 'auto_'+option, 'manual_'+option, 'without_'+option, 'auto_vs_wo_speedup', 'auto_vs_manual_%diff'])
        model_ = []
        auto_ = []
        manual_ = []
        without_ = []
        for line in auto:
            line = line.split()
            model_.append(line[1])
            auto_.append(line[5])

        for line in manual:
            line = line.split()
            manual_.append(line[5])

        for line in wo:
            line = line.split()
            without_.append(line[5])

        for i in range(len(model_)):
            if float(without_[i])==0:
                auto_vs_wo_speedup='x'
                auto_vs_manual_diff='x'
            else:
                auto_vs_wo_speedup = '%.6f' % (float(auto_[i]) / float(without_[i]))
                auto_vs_manual_diff = '%.6f' % abs((float(manual_[i]) - float(without_[i])) / float(without_[i]))
            lists = [model_[i], auto_[i], manual_[i], without_[i], auto_vs_wo_speedup, auto_vs_manual_diff]
            writer.writerows([lists])


generated_report(auto_jit, manual_jit, wo_jit,'jit')
generated_report(auto_eager, manual_eager, wo_eager,'eager')
