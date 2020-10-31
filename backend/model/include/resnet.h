#ifndef RESNET
#define RESNET

#include <torch/torch.h>
#include "loss.h"

#ifdef __cplusplus
extern "C"
{
#endif //__cplusplus

enum Layer{ CONV64, CONV128, CONV256, CONV512, MAXPOOL, AVGPOOL };

    class resNetImpl : public torch::nn::Module {

        public:
            resNetImpl(const std::vector<Layer>& config, const::set<size_t>& selected, bool batch_norm, const std::string& scriptmodule_file_path);
            std::vector<torch::Tensor> forward(torch::Tensor x);
            void set_selected_layer_idxs(const std::set<size_t>& idxs){ selected_layer_idxs_= idxs; }
            std::set<size_t> get_selected_layer_idxs() const { return selected_layer_idxs_; }

        private:
            torch::nn::Sequential make_layers(const std::vector<Layer>& config, bool batch_norm);

            torch::nn::Sequential layers;
            std::set<size_t> selected_layer_idxs_;

    };
    TORCH_MODULE(resNet);


    class resNet18Impl : public resNetImpl {

        public:
            resNet18Impl(const std::string& scriptmodule_file_path = {}, const std::set<size_t>& selected_layer_idxs = {0, 5, 10, 19, 28}); 
    
    };
    TORCH_MODULE(resNet18);

#ifdef __cplusplus
}
#endif //__cplusplus


#endif // RESNET