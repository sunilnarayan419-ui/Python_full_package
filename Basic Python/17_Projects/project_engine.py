
import math, statistics, json
from collections import Counter, defaultdict, deque
from pathlib import Path

def run(kind, x):
    if kind == "nucleotide":
        s=x.upper()
        if set(s)-set("ATGC"): raise ValueError("DNA must contain A,T,G,C only")
        counts={b:s.count(b) for b in "ATGC"}
        print("Length:",len(s),"Counts:",counts,"Frequencies:",{b:round(v/len(s),4) for b,v in counts.items()} if s else {})
    elif kind == "gc":
        s=x.upper()
        if set(s)-set("ATGC"): raise ValueError("DNA must contain A,T,G,C only")
        print("GC%:",round(100*(s.count("G")+s.count("C"))/len(s),3) if s else 0)
    elif kind == "revcomp":
        s=x.upper()
        if set(s)-set("ATGC"): raise ValueError("DNA must contain A,T,G,C only")
        print("Reverse complement:",s.translate(str.maketrans("ATGC","TACG"))[::-1])
    elif kind == "transcribe":
        s=x.upper()
        if set(s)-set("ATGC"): raise ValueError("DNA must contain A,T,G,C only")
        print("RNA:",s.replace("T","U"))
    elif kind == "codons":
        s=x.upper()
        print("Codon counts:",dict(Counter(s[i:i+3] for i in range(0,len(s)-2,3))),"Trailing bases:",len(s)%3)
    elif kind == "motif":
        s,m=x
        print("0-based motif positions:",[i for i in range(len(s)-len(m)+1) if s[i:i+len(m)]==m])
    elif kind == "hamming":
        a,b=x
        if len(a)!=len(b): raise ValueError("Sequences must have equal lengths")
        print("Hamming distance:",sum(a1!=b1 for a1,b1 in zip(a,b)))
    elif kind == "kmer":
        s,k=x
        if not 1<=k<=len(s): raise ValueError("k must be between 1 and sequence length")
        print("K-mer counts:",dict(Counter(s[i:i+k] for i in range(len(s)-k+1))))
    elif kind == "homopolymer":
        if not x: print("Empty sequence"); return
        best=cur=x[0]
        for c in x[1:]:
            cur=cur+c if c==cur[-1] else c
            if len(cur)>len(best): best=cur
        print("Longest run:",best,"Length:",len(best))
    elif kind == "fasta":
        records={}; current=None
        for line in x.splitlines():
            line=line.strip()
            if not line: continue
            if line.startswith(">"): current=line[1:]; records[current]=""
            elif current is None: raise ValueError("Sequence appears before FASTA header")
            else: records[current]+=line
        print("Records:",json.dumps(records,indent=2))
    elif kind == "allele":
        n=sum(x.values())
        if n<=0: raise ValueError("Genotype count total must be positive")
        p=(2*x.get("AA",0)+x.get("Aa",0))/(2*n)
        print("p(A):",p,"q(a):",1-p)
    elif kind == "hwe":
        p=x
        if not 0<=p<=1: raise ValueError("p must be in [0,1]")
        print({"AA":p*p,"Aa":2*p*(1-p),"aa":(1-p)**2})
    elif kind == "exponential":
        n0,r,t=x
        print("N(t):",n0*math.exp(r*t))
    elif kind == "mm":
        vmax,km,subs=x
        print("Rates:",{s:round(vmax*s/(km+s),4) if km+s else None for s in subs})
    elif kind == "buffer":
        pka,base,acid=x
        if base<=0 or acid<=0: raise ValueError("Concentrations must be positive")
        print("pH:",pka+math.log10(base/acid))
    elif kind == "decay":
        c0,k,times=x
        print("Concentrations:",{t:round(c0*math.exp(-k*t),4) for t in times})
    elif kind == "shannon":
        total=sum(x.values())
        if total<=0: raise ValueError("Counts must total more than zero")
        print("Shannon H:",-sum((v/total)*math.log(v/total) for v in x.values() if v))
    elif kind == "diagnostics":
        tp,fn,tn,fp=(x[k] for k in ("TP","FN","TN","FP"))
        ratio=lambda a,b:a/b if b else None
        print({"sensitivity":ratio(tp,tp+fn),"specificity":ratio(tn,tn+fp),"PPV":ratio(tp,tp+fp),"NPV":ratio(tn,tn+fn)})
    elif kind == "stats":
        print("n:",len(x),"Mean:",statistics.mean(x),"Median:",statistics.median(x),"Sample SD:",statistics.stdev(x) if len(x)>1 else None)
    elif kind == "correlation":
        a,b=x
        if len(a)!=len(b) or len(a)<2: raise ValueError("Need equal-length paired lists")
        ma,mb=statistics.mean(a),statistics.mean(b)
        num=sum((u-ma)*(v-mb) for u,v in zip(a,b))
        den=math.sqrt(sum((u-ma)**2 for u in a)*sum((v-mb)**2 for v in b))
        print("Pearson r:",num/den if den else None)
    elif kind == "regression":
        a,b=x
        if len(a)!=len(b) or len(a)<2: raise ValueError("Need equal-length paired lists")
        ma,mb=statistics.mean(a),statistics.mean(b)
        den=sum((u-ma)**2 for u in a)
        if not den: raise ValueError("Predictor variance must be positive")
        slope=sum((u-ma)*(v-mb) for u,v in zip(a,b))/den
        intercept=mb-slope*ma
        print("Slope:",slope,"Intercept:",intercept,"Predictions:",[intercept+slope*u for u in a])
    elif kind == "hill":
        emax,ec50,h,doses=x
        print("Responses:",{d:round(emax*d**h/(ec50**h+d**h),4) if d>0 else 0 for d in doses})
    elif kind == "bfs":
        graph=defaultdict(list)
        for a,b in x["edges"]: graph[a].append(b); graph[b]
        start,target=x["start"],x["target"]; queue=deque([start]); prev={start:None}
        while queue:
            u=queue.popleft()
            if u==target: break
            for v in graph[u]:
                if v not in prev: prev[v]=u; queue.append(v)
        if target not in prev: print("No path found")
        else:
            path=[]; u=target
            while u is not None: path.append(u); u=prev[u]
            print("Shortest path:",path[::-1])
    elif kind == "degree":
        indeg=Counter(); outdeg=Counter(); nodes=set()
        for a,b in x: nodes.update((a,b)); outdeg[a]+=1; indeg[b]+=1
        print({n:{"in":indeg[n],"out":outdeg[n]} for n in sorted(nodes)})
    elif kind == "groups":
        groups=defaultdict(list)
        for group,value in x: groups[group].append(value)
        print("Group summaries:",{k:{"n":len(v),"mean":statistics.mean(v)} for k,v in groups.items()})
    else:
        raise ValueError("Unknown project algorithm: "+kind)
