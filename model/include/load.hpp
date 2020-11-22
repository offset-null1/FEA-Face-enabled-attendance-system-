#ifndef __LOAD__
#define __LOAD__

#include <opencv2/core.hpp>
#include <opencv2/hdf.hpp>
#include <torch/torch.h>
#include <torch/data/datasets/base.h>
#include <tuple>
#include <array>

#ifdef __cplusplus
extern "C"{
#endif // __cplusplus

    namespace loader{
        cv::Mat load_HDF5(std::string&& path, std::string&& delimiter);
        torch::Tensor data_toTensor(std::string&& dataset_path);
        torch::Tensor label_toTensor(std::string&& dataset_path);

        class loadDataset : public torch::data::datasets::Dataset<loadDataset, torch::Tensor> {

            private:
                torch::Tensor data, labels;

            public:
                loadDataset(std::string&& dataset_path, std::string&& label_path, size_t batch_size) {

                   data = data_toTensor(std::move(dataset_path));
                   labels = label_toTensor(std::move(label_path));

                }

                std::tuple<torch::Tensor, torch::Tensor> get_(size_t index)  {
                    
                    return { data[index], labels[index]};
                }

                //  optional<size_t> size() const override {
                //   return data.size();
                // }

        };
    } 

#ifdef __cplusplus
}
#endif // __cplusplus
#endif // !_LOAD__