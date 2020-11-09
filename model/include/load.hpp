#ifndef __LOAD__
#define __LOAD__

#include <opencv2/core.hpp>
#include <opencv2/hdf.hpp>
#include <torch/torch.h>

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

            public:
                loadDataset(std::string&& file_name, const std::string& parent_name, const std::string& image_dataset, const std::string& label_dataset) {

                   images = loader::data_toTensor(std::string&& file_name, const std::string& parent_name, const std::string& image_dataset);
                   labels = loader::label_toTensor(std::string&& file_name, const std::string& parent_name, const std::string& label_dataset);

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