from math import sqrt

mean = lambda l: sum(l)/len(l)

sqrt_3 = 1.73205080757

m1 = lambda mpe, k, m: mpe / k / m

m2 = lambda m, l:(max(l) - min(l)) / 2 / sqrt_3 / m

m4 = lambda t, w, k, n: (t - 20) * w / k * sqrt(n)

m6 = lambda m, v, k: sqrt(sum([m1(m0, v0, k)**2 for m0, v0 in zip(m, v)]))

def m7(p, A, P, p_0):
    n = len(A)
    p = p * (n/len(p))
    p_ = mean(p)
    A_= mean(A)
    Sxy = sum([(p0-p_)*(A0-A_) for p0, A0 in zip(p, A)])
    Sxx = sum([(p0-p_)**2 for p0 in p])
    b = Sxy/Sxx
    a = A_ - b*p_
    s = sqrt(sum([(A0-a-b*p0)**2 for A0, p0 in zip(A, p)])/(n-2))
    u_p0 = s/b*sqrt(1/P+1/n+(p_0-p_)**2/Sxx)
    return u_p0/p_0

mf = lambda us, w, k: sqrt(sum([u**2 for u in us]))*w*k