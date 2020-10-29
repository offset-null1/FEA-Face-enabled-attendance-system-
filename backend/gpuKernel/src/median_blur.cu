#include <iostream>
#include <stdio.h>
#include <cuda.h>
#include <cuda_runtime_api.h>
#include <device_launch_parameters.h>
#include <opencv2/highgui.hpp>
#include <math.h>

#define TILE_SIZE 4

#define gpuErrchk(ans) { gpuAssert((ans), __FILE__, __LINE__); }
inline void gpuAssert(cudaError_t code, const char *file, int line, bool abort=true) {
    if(code != cudaSuccess){
        std::cerr << "GPU assert:" << file <<":"<< line<<":"<< cudaGetErrorString(code) <<"\n";
        if(abort) exit(code);
    }
}

__global__ void kernel(unsigned char *in, unsigned char* out, uint frameWidth, uint frameHeight){

   uint col = blockDim.x * blockIdx.x + threadIdx.x;
   uint row = blockDim.y * blockIdx.y + threadIdx.y;

    __shared__ unsigned char window[(TILE_SIZE + 2)][(TILE_SIZE + 2)];

    bool is_xleft = (threadIdx.x == 0) , is_xright = (threadIdx.x == TILE_SIZE - 1);
    bool is_ytop = (threadIdx.y == 0) , is_ybottom = (threadIdx.y == TILE_SIZE - 1);

    //initialize boundary conditions (for all tiles) padding = 0

    if(is_xleft)  { window[threadIdx.x][threadIdx.y + 1] = 0; }

    else if(is_xright) { window[threadIdx.x + 2][threadIdx.y + 1] = 0; }
    
    if(is_ytop)   { window[threadIdx.x + 1][threadIdx.y] = 0; 

        if(is_xleft) { window[threadIdx.x][threadIdx.y] = 0; }
        else if(is_xright) { window[threadIdx.x + 2][threadIdx.y] = 0; }
    }
   
    else if(is_ybottom) { window[threadIdx.x + 1][threadIdx.y + 2] = 0; 

        if(is_xleft) { window[threadIdx.x][threadIdx.y + 2] = 0; }
        else if(is_xright) { window[threadIdx.x + 2][threadIdx.y + 2] = 0; }
    }
    
    //store frame values except paddings 
    window[threadIdx.x + 1][threadIdx.y + 1] = in[((row * frameWidth)) + col];
    
    //check if middle tiles then populate the padding values
    if(is_xleft && (col>0)) { window[threadIdx.x][threadIdx.y + 1] = in[(row * frameWidth) + (col-1)]; }

    else if(is_xright && (col<(frameWidth-1))) { window[threadIdx.x + 2][threadIdx.y + 1] = in[(row * frameWidth) + (col+1)]; }

    if(is_ytop && (row>0)){
        window[threadIdx.x + 1][threadIdx.y] = in[((row-1) * frameWidth) + col];

        if(is_xleft) { window[threadIdx.x][threadIdx.y] = in[((row-1) * frameWidth) + (col-1)]; }
        else if(is_xright) { window[threadIdx.x+2][threadIdx.y] = in[((row-1) * frameWidth) + (col+1)]; }

    } 

    else if(is_ybottom && row<(frameHeight-1)){
        window[threadIdx.x + 1][threadIdx.y + 2] = in[((row+1) * frameWidth) + col];

        if(is_xleft) {window[threadIdx.x][threadIdx.y + 2] = in[((row+1) * frameWidth) + (col-1)]; }
        else if(is_xright) {window[threadIdx.x+2][threadIdx.y + 2] = in[((row+1) * frameWidth) + (col+1)]; }

    } 

    __syncthreads();

    //end storing

    //filter setup
    if(col<(frameWidth-1) && row<(frameHeight-1)){
        unsigned char filterWindow[9] = { window[threadIdx.x][threadIdx.y]    , window[threadIdx.x + 1][threadIdx.y]    , window[threadIdx.x+2][threadIdx.y]      ,
            window[threadIdx.x][threadIdx.y + 1], window[threadIdx.x + 1][threadIdx.y + 1], window[threadIdx.x + 2][threadIdx.y + 1],
            window[threadIdx.x][threadIdx.y + 2], window[threadIdx.x + 1][threadIdx.y + 2], window[threadIdx.x + 2][threadIdx.y + 2]  };

//sort
    
        for(uint i=0 ; i<9 ; ++i){
            for(uint j=i+1 ; j<9 ; ++j){
                if(filterWindow[i] > filterWindow[j]){
                    unsigned char temp = filterWindow[i];
                    filterWindow[i]    = filterWindow[j];
                    filterWindow[j]    = temp;
                }
            }
        }
    
        out[(row * frameWidth) + col] = filterWindow[4]; //store median
    }

}


extern "C"{

    void take_input(const cv::Mat& in_frame, const cv::Mat& out_frame){
        unsigned char* in;
        unsigned char* out;
        uint frameWidth = in_frame.cols;
        uint frameHeight = in_frame.rows;
    
        size_t d_ipSize = in_frame.cols * in_frame.rows;
        size_t d_outSize = (in_frame.cols/2) * (in_frame.rows/2);
    
        cudaEvent_t start,stop;
    
        gpuErrchk( cudaEventCreate(&start) );
        gpuErrchk( cudaEventCreate(&stop) );
        gpuErrchk( cudaEventRecord(start) );
      
        gpuErrchk( cudaMalloc( (void**)& in, d_ipSize) );
        gpuErrchk( cudaMalloc( (void**)& out, d_ipSize) );

        gpuErrchk( cudaMemcpy( in, in_frame.data, d_ipSize, cudaMemcpyHostToDevice) );                  
   
        dim3 threads(TILE_SIZE, TILE_SIZE);                                                                  
        dim3 blocks( (in_frame.cols /threads.x)+1 , (in_frame.rows /threads.y)+1 );
    
        kernel <<< blocks,threads >>> (in, out, frameWidth, frameHeight);
    
        gpuErrchk( cudaDeviceSynchronize() );
    
        gpuErrchk( cudaMemcpy( out_frame.data, out, d_ipSize, cudaMemcpyDeviceToHost ) );
    
        cudaFree(in);
        cudaFree(out);
    
        gpuErrchk( cudaEventRecord(stop) );
        float time = 0;
        cudaEventElapsedTime(&time, start, stop);
    
        // std::cout<<"Time :"<<time<<"\n";
        printf("time %f\n", time); 
       
    }
}
