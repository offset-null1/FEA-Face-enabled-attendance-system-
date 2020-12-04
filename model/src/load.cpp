#include <experimental/filesystem>
#include <opencv2/core.hpp>
#include <opencv2/hdf.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <torch/torch.h>
#include <iostream>
#include <string>
#include "load.hpp"

namespace fs = std::experimental::filesystem;

std::vector<std::string> split_path(std::string&& path, const std::string& delimiter){
    std::string token;
    std::vector<std::string> p;

    if(!path.find('/',0))
        path = fs::absolute(path); 

    while( auto pos = path.find(delimiter) != std::string::npos ){
        token = path.substr(0,pos);
        p.push_back(token);
        path.erase(0,pos+delimiter.length());
    }
    return p;
}
namespace loader{

    namespace fs = std::experimental::filesystem;

    cv::Mat load_HDF5(std::string&& hdf5_path){

        cv::Mat data;
        std::vector<std::string> file_name = split_path(std::move(hdf5_path), "/");
        if( file_name[file_name.size()-1].find(".h5") ){
            
            cv::Ptr<cv::hdf::HDF5> h5io = cv::hdf::open(hdf5_path);

            if(h5io->hlexists(file_name[1]) && h5io->hlexists(file_name[2]))
                h5io->dsread(data, file_name[2]);

            h5io->close();
        }
        return data;
    }

    torch::Tensor data_toTensor(std::string&& file_path){ //need to check for dataset dim
        
        cv::Mat img_data = load_HDF5(std::move(file_path));

        if(!(img_data.at<cv::Vec3b>(0).rows == img_data.at<cv::Vec3b>(0).cols == 224))
            cv::resize(img_data, img_data, cv::Size(224,224), cv::INTER_CUBIC);
        
        torch::Tensor img_tensor = torch::from_blob(img_data.data, {img_data.size[img_data.dims-4], img_data.size[img_data.dims-3], img_data.size[img_data.dims-2], img_data.size[img_data.dims-1] }, torch::kByte);
        img_tensor = img_tensor.permute({3,2,0,1});

        return img_tensor;
    }

    torch::Tensor label_toTensor(std::string&& file_path){

        cv::Mat label_data = load_HDF5(std::move(file_path));
        
        // if(data.dims == 1)
        torch::Tensor label_tensor = torch::from_blob(label_data.data, {label_data.cols}, torch::kByte);

        return label_tensor;
    }


}//loader
