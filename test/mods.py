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


if __name__ == '__main__':
    u= [
        m1(0.0002, sqrt_3, 0.5036),
        m2(19.4, [19.6, 19.5, 18.3, 19.6, 20.4, 18.6, 20.2, 18.9, 19.7, 20.0, 18.8]),
        m1(0.03, sqrt_3, 25),
        m4(23, 2.1/1000, sqrt_3, 6),
        m1(3, sqrt_3, 1000),
        m6([0.02,0.10,0.10,0.015,0.025,0.03], [10,100,100,5,5,25], sqrt_3),
        m7([0,0.2,0.4,0.6,0.8,1.0],[0.0017,0.0185,0.0345,0.0536,0.0696,0.0859,0.0006,0.0189,0.0349,0.0517,0.0698,0.0876,0.0000,0.0181,0.0349,0.0528,0.0692,0.0842,0.0030,0.0165,0.0349,0.0537,0.0701,0.0868], 3, 0.42)
        ]
    print u
    print mf(u, 20.8, 2)