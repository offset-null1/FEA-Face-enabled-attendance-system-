#ifndef __LOAD__
#define __LOAD__

#include <opencv2/core.hpp>
#include <opencv2/hdf.hpp>
#include <torch/torch.h>
#include <torch/data/datasets/base.h>
#include <torch/data/example.h>
#include <tuple>
#include <array>

#ifdef __cplusplus
extern "C"{
#endif // __cplusplus

    namespace loader{
        cv::Mat load_HDF5(std::string&& path, std::string&& delimiter);
        torch::Tensor data_toTensor(std::string&& dataset_path);
        torch::Tensor label_toTensor(std::string&& dataset_path);

        class loadDataset : public torch::data::datasets::Dataset<loadDataset> {   //< custom_dataset, Example<torch::Tensor, torch::Tensor> >

            private:
                torch::Tensor data, labels;

            public:
                loadDataset(std::string&& dataset_path, std::string&& label_path) {
                    data = data_toTensor(std::move(dataset_path));
                    labels = label_toTensor(std::move(label_path));

                }

                torch::data::Example<> get(size_t index) override {
                    
                    return { data[index], labels[index]};
                }

                torch::optional<size_t> size() const override {
                    return data.size(0);
                }

        };
    } 

#ifdef __cplusplus
}
#endif // __cplusplus
#endif // !_LOAD__