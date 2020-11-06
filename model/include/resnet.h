#ifndef RESNET
#define RESNET

#include <torch/torch.h>
#include <vector>
#include "loss.h"

#ifdef __cplusplus
extern "C"
{
#endif //__cplusplus

struct baseBlockImpl : torch::nn::Module{
 
    baseBlockImpl(int64_t in_channel, int64_t out_channel, int64_t stride=1);
    torch::Tensor forward(torch::Tensor x);
    
    static const int num_seq;

    int64_t stride;
    torch::nn::Conv2d conv1;
    torch::nn::BatchNorm bn1;
    torch::nn::Conv2d conv2;
    torch::nn::BatchNorm bn2;
    torch::nn::Sequential downsample = torch::nn::Sequential();    

};
TORCH_MODULE(baseBlock);


struct resnetImpl : torch::nn::Module{

    resnetImpl(std::vector<int64_t> layers, int64_t classes );
    void init_weight();
    torch::Tensor forward(torch::Tensor x);

    int64_t inplanes = 64;
    int64_t num_layers = 4;
    torch::nn::Conv2d conv1;
    torch::nn::BatchNorm bn1;
    torch::nn::Sequential layer1;
    torch::nn::Sequential layer2;
    torch::nn::Sequential layer3;
    torch::nn::Sequential layer4;
    torch::nn::Linear fc;

};
TORCH_MODULE(resnet);

#ifdef __cplusplus
}
#endif //__cplusplus


#endif // RESNET