import numpy as np, glob
from PIL import Image
fs=sorted(glob.glob('flow/g*.png'))
def load(f): return np.asarray(Image.open(f),dtype=np.float32)
def pc(a,b):
    A=np.fft.fft2(a-a.mean());B=np.fft.fft2(b-b.mean())
    R=A*np.conj(B);R/=np.abs(R)+1e-9;r=np.fft.ifft2(R).real
    y,x=np.unravel_index(r.argmax(),r.shape);h,w=r.shape
    if y>h//2:y-=h
    if x>w//2:x-=w
    return x,y,r.max()
def lap(a):
    l=-4*a[1:-1,1:-1]+a[:-2,1:-1]+a[2:,1:-1]+a[1:-1,:-2]+a[1:-1,2:]
    return l.var()
prev=None;rows=[]
for i,f in enumerate(fs):
    a=load(f);t=520+i/10
    if prev is not None:
        dx,dy,pk=pc(prev,a);mad=np.abs(a-prev).mean()
    else: dx=dy=pk=mad=0
    rows.append((t,dx,dy,pk,mad,lap(a),a.mean()));prev=a
open('flow_520_546.csv','w').write('t,dx_px,dy_px,pc_peak,mean_abs_diff,laplacian_var,mean_luma\n'+'\n'.join(','.join(f'{v:.3f}' for v in r) for r in rows))
for r in rows[::5]: print(' '.join(f'{v:8.2f}' for v in r))
