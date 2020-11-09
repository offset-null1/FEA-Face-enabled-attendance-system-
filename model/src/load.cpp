#include <experimental/filesystem>
#include <opencv2/core.hpp>
#include <opencv2/hdf.hpp>
#include <torch/torch.h>
#include <iostream>
#include <string>

namespace load{

    namespace fs = std::experimental::filesystem;

    cv::Mat load_HDF5(std::string&& file_name, const std::string& parent_name, const std::string& dataset_name){

        cv::Mat data;
        if( file_name.find(".h5", file_name.length()-3) ){
            if(!file_name.find('/',0))
                file_name = fs::absolute(file_name); 

            cv::Ptr<hdf::HDF5> h5io = cv::hdf::open(file_name);

            if(h5io->hlexists(parent_name) && h5io->hlexists(dataset_name))
                h5io->dsread(data, dataset_name);

            h5io->close();
        }
        return data;
    }

    torch::Tensor data_toTensor(cv::Mat&& data){ //need to check for dataset dim
        
        if(!(data[0].rows == data[0].cols == 224))
            cv::resize(img_data, img_data, cv::Size(224,224), cv::INTER_CUBIC);
        
        torch::Tensor tensor_tensor = torch::from_blob(img_data.data, {img_data.rows, img_data.cols, img_data.channels, img_data.size(img_data.dims - 1) }, torch::kBytes);
        img_tensor = img.tensor.permute({3,2,0,1});

        return img_tensor;
    }

    torch::Tensor label_toTensor(cv::Mat&& data ){ //will throw runtime err if cond not true, needs log

        if(data.dims == 1)
            torch::Tensor labels = torch::full({1}, data);

        return labels;
    }

}


int main(){

    
    return 0;
}