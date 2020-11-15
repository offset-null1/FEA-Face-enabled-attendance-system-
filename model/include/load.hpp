#ifndef __LOAD__
#define __LOAD__

#include <opencv2/core.hpp>
#include <opencv2/hdf.hpp>
#include <torch/torch.h>
#include <tuple>

#ifdef __cplusplus
extern "C"{
#endif // __cplusplus

    namespace loader{
        cv::Mat load_HDF5(std::string&& file_name, const std::string& parent_name, const std::string& dataset_name);
        torch::Tensor data_toTensor(cv::Mat&& data);
        torch::Tensor label_toTensor(cv::Mat&& data);

        class loadDataset : public torch::data::dataset<loadDataset> {

            private:
                torch::Tensor images, labels;
                size_t batch_size;
                int16_t counter = 0;

            public:
                loadDataset(std::string&& dataset_path, std::string&& label_path, size_t batch_size):batch_size(batch_size) {

                   images = loader::data_toTensor(std::move(dataset_path));
                   labels = loader::label_toTensor(std::move(label_path));

                }

                torch::dataset::Example<> get(size_t index) override {

                    return { images.at(index).clone(), labels.at(index).clone() };
                }

                torch::optional<size_t> size() const override {
                    return labels.size();
                }

        };
    } 

#ifdef __cplusplus
}
#endif // __cplusplus
#endif // !_LOAD__