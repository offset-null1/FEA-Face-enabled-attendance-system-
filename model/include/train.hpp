#ifndef __TRAIN__
#define __TRAIN__

#include <torch/torch.h>
#include <torch/script.h>
#include "load.hpp"

// #ifdef __cplusplus
// extern "C"{
// #endif //__cplusplus
    template<typename Dataloader>
    void train_net(Dataloader& data_loader, torch::jit::script::Module net, torch::optim::Optimizer& optimizer, torch::nn::Linear lin,const int epochs, size_t dataset_size);

// #ifdef __cplusplus
// }
// #endif // __cplusplus
#endif // !__TRAIN__