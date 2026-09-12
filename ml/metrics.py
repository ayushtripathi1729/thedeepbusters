import math
def binary_metrics(labels, scores, threshold=.5):
    if len(labels)!=len(scores) or not labels: raise ValueError("matching non-empty labels/scores required")
    tp=sum(y==1 and p>=threshold for y,p in zip(labels,scores)); tn=sum(y==0 and p<threshold for y,p in zip(labels,scores)); fp=sum(y==0 and p>=threshold for y,p in zip(labels,scores)); fn=sum(y==1 and p<threshold for y,p in zip(labels,scores))
    precision=tp/(tp+fp) if tp+fp else 0; recall=tp/(tp+fn) if tp+fn else 0
    return {"accuracy":(tp+tn)/len(labels),"precision":precision,"recall":recall,"f1":2*precision*recall/(precision+recall) if precision+recall else 0,"balanced_accuracy":((tp/(tp+fn) if tp+fn else 0)+(tn/(tn+fp) if tn+fp else 0))/2,"false_positive_rate":fp/(fp+tn) if fp+tn else 0,"false_negative_rate":fn/(fn+tp) if fn+tp else 0,"confusion_matrix":[[tn,fp],[fn,tp]]}
def expected_calibration_error(labels,scores,bins=15):
    total=len(labels); value=0
    for i in range(bins):
        lo,hi=i/bins,(i+1)/bins; bucket=[(y,p) for y,p in zip(labels,scores) if lo<=p<(hi if i<bins-1 else 1.000001)]
        if bucket:value+=len(bucket)/total*abs(sum(p for _,p in bucket)/len(bucket)-sum(y for y,_ in bucket)/len(bucket))
    return value
