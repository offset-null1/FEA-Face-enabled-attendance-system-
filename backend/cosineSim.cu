#include<iostream>
#include<cuda_runtime.h>

#define nThreads 512
#define nBlocks 49
#define N nThreads*nBlocks

__global__ void dot(double *d_a,double *d_b,double *d_o){

    int t_id = threadIdx.x;
    int g_id = blockDim.x * blockIdx.x + threadIdx.x;
    int incr = gridDim.x * blockIdx.x;

    __shared__ double cache[nThreads];
    double temp=0.0;

    while(g_id < N){
        temp += d_a[g_id] * d_b[g_id];
        g_id += incr;
    }
    cache[t_id] = temp;
    __syncthreads();

    uint offset = blockDim.x/2;
    while(offset != 0){
        if(t_id < offset){
            cache[t_id] += cache[t_id+offset];
        }
        offset/=2;
        __syncthreads();
    }
    if(t_id==0){
        *d_o=cache[0];
    }   
}
 

__global__ void magnitude(double *d_a,double *d_o) {
   uint t_id = threadIdx.x;
   uint g_id = blockDim.x * blockIdx.x + threadIdx.x;
   uint incr = gridDim.x * blockIdx.x;

   __shared__ double sq[nThreads];
   double temp = 0.0;
   while(g_id<N){
        temp = pow(d_a[g_id],2);
        g_id += incr;
   }
   sq[t_id]= temp;
   __syncthreads();

   uint offset = blockDim.x/2;
   while(offset != 0){
       if(t_id < offset){
           sq[t_id] += sq[t_id+offset];
       }
       offset /= 2;
       __syncthreads();
   }
   if(t_id ==0){
       sq[0] = sqrt(sq[0]);
        *d_o = sq[0];
   }
}

int main(void)
{   
    double result=0.0;

    double a[] = {1.,2.,3.};
    double b[] = {1.,2.,3.};
    double dot,mag_a,mag_b;
    double  *d_a, *d_b, *d_o;
    int size= 3* sizeof(double);

    cudaStream_t stream1,stream2,stream3;
    // cudaError_t flag;

    cudaStreamCreate(&stream1);
    cudaStreamCreate(&stream2);
    cudaStreamCreate(&stream3);

    cudaMalloc((void**)&d_a, size);
    cudaMalloc((void**)&d_b, size);
    cudaMalloc((void**)&d_o, size);

    cudaMemcpyAsync(&d_a, &a, size, cudaMemcpyHostToDevice,stream1);
    cudaMemcpyAsync(&d_b, &b, size, cudaMemcpyHostToDevice,stream1);
    dot<<<nBlocks,nThreads,0,stream1>>>(d_a,d_b,d_o);
    cudaMemcpyAsync(&dot, &d_o, sizeof(double), cudaMemcpyDeviceToHost, stream1);

    cudaMemcpyAsync(&d_a, a, size, cudaMemcpyHostToDevice,stream2);
    magnitude<<<nBlocks,nThreads,0,stream2>>>(d_a,d_o);
    cudaMemcpyAsync(&mag_a, &d_o, sizeof(double), cudaMemcpyDeviceToHost, stream2);

    cudaMemcpyAsync(&d_b, b, size, cudaMemcpyHostToDevice,stream3);
    magnitude<<<nBlocks,nThreads,0,stream3>>>(d_b,d_o);
    cudaMemcpyAsync(&mag_b, &d_o, sizeof(double), cudaMemcpyDeviceToHost, stream3);

    cudaDeviceSynchronize();
    
    result = dot/(mag_a*mag_b);
    std::cout<<"Result: "<<result<<std::endl;
    // cudaFree(d_a); cudaFree(d_b); cudaFree(d_o);
    
    return 0;
}