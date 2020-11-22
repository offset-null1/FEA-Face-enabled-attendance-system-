#ifndef __TRAIN__
#define __TRAIN__

#include <torch/torch.h>
#include <torch/script.h>
#include "load.hpp"

#ifdef __cplusplus
extern "C"{
#endif //__cplusplus

    void train_net(loader::loadDataset& data_loader, torch::jit::script::Module net, torch::nn::Linear fc, const int epochs, bool use_default_loss, bool test);

#ifdef __cplusplus
}
#endif // __cplusplus
#endif // !__TRAIN__