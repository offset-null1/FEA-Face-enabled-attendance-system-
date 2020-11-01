#ifndef RESNET
#define RESNET

#include <torch/torch.h>
#include "loss.h"

#ifdef __cplusplus
extern "C"
{
#endif //__cplusplus

struct baseBlock : torch::nn::Module{
 
    baseBlock(int64_t in_channel, int64_t out_channel, int64_t stride=1 );
    torch::Tensor forward(torch::Tensor x);
    
    static const int num_seq;

    int64_t stride;
    torch::nn::Conv2d conv1;
    torch::nn::BatchNorm bn1;
    torch::nn::Conv2d conv2;
    torch::nn::BatchNorm bn2;
    torch::nn::Sequential residual;    

};
template<class num_seq>
struct resnet : torch::nn::module{

    resnet(torch::IntList layers, int64_t classes );
    void init_weight();
    torch::Tensor forward(torch::Tensor x);

    int64_t inplanes = 64;
    torch::nn::Conv2d conv1;
    torch::nn::BatchNorm bn1;
    torch::nn::Sequential layer1;
    torch::nn::Sequential layer2;
    torch::nn::Sequential layer3;
    torch::nn::Sequential layer4;
    torch::nn::Linear fc;


};
git
#ifdef __cplusplus
}
#endif //__cplusplus


#endif // RESNET