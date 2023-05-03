import os
def Param(name='', *args, **kwargs):
    return name

def report_kfolds(log):
    kfolds = log['kfolds']
    params = kfolds['params']
    rmses = kfolds['rmse']
    best_param = kfolds['best_param']
    header = '|Parameter|RMSE|\n|:-----:|:---|\n'
    report = header
    for i in range(0, len(params)):
        line = ''
        for item in params[i]:
            line += '`{}={}`, '.format(item, str(params[i][item]))
        line = line[:-2]
        
        if params[i] == best_param:
            line = '|**'+line+'**'
        else:
            line = '|'+line
        
        if params[i] == best_param:
            line += '|**{:.4f}**|\n'.format(rmses[i])
        else:
            line += '|{:.4f}|\n'.format(rmses[i])
        report += line
    return report

def report_perf(log):
    report = '|Fold|RMSE|$R^2$|\n|:---:|:---|:---|\n'
    report += '|Train|{:.4f}|{:.4f}|\n'.format(log['train']['rmse'],
                                               log['train']['r2'])
    report += '|Test|{:.4f}|{:.4f}|\n'.format(log['test']['rmse'],
                                               log['test']['r2'])
    return report

def report(log):
    content = ''
    content += '## Comparison\n'
    content += '|Model|Train RMSE|Train $R^2$|Test RMSE|Test $R^2$|\n|:--|:---|:---|:---|:---|\n'
    for model in log:
        content += '|{}|{:.4f}|{:.4f}|{:.4f}|{:.4f}|\n'.format(model,
                                                             log[model]['train']['rmse'],
                                                             log[model]['train']['r2'],
                                                             log[model]['test']['rmse'],
                                                             log[model]['test']['r2'])
    content += '## Models\n'
    for model in log:
        content += '### {}\n'.format(model)
        content += '#### K-Folds\n'
        content += report_kfolds(log[model])
        content += '#### Performance\n'
        content += report_perf(log[model])
    return content

def get_log(logs=[]):
    log_full = {}
    for log_path in logs:
        with open(log_path, 'r') as f:
            log = f.read()
            log = eval(log)
            for model in log:
                log_full[model] = log[model]
    return log_full

def create_report(path, logs=[]):
    with open(path, 'w') as f:
        f.write(report(get_log(logs)))
        
def get_log_list(path):
    log_list = []
    for root, _, files in os.walk(path):
        for file in files:
            log_list.append(os.path.join(root, file))
            
    return log_list

if __name__ == '__main__':
    create_report('./report.md', get_log_list('../models/'))