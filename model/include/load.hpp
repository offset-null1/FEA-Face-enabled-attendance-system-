#ifndef __LOGGING__
#define __LOGGING__

#include <opencv2/core.hpp>
#include <opencv2/hdf.hpp>
#include <torch/torch.h>

#ifdef __cplusplus
extern "C"{
#endif // __cplusplus

namespace load
{
    cv::Mat load_HDF5(std::string&& file_name, const std::string& parent_name, const std::string& dataset_name);
    torch::Tensor data_toTensor(cv::Mat&& data);
    torch::Tensor label_toTensor(cv::Mat&& data);
}

#ifdef __cplusplus
}
#endif // __cplusplus
#endif // !__LOGGING__