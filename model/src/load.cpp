#include <experimental/filesystem>
#include <opencv2/core.hpp>
#include <opencv2/hdf.hpp>
#include <torch/torch.h>
#include <iostream>
#include <string>

static std::vector<std::string> split_path(std::string&& path, std::string&& delimiter){
    std::string token;
    std::vector<std::string> p;

    if(!path.find('/',0))
        path = fs::absolute(file_name); 

    while( (pos = s.find(delimiter)) != std::string::npos){
        token = s.substr(0,pos);
        p.push_back(token);
        s.erase(0,pos+delimiter.length());
    }
    return p;
}
namespace loader{

    namespace fs = std::experimental::filesystem;

    cv::Mat load_HDF5(std::string&& hdf5_path){

        cv::Mat data;
        std::vector<std::string> file_name = split_path(std::move(hdf5_path), "/");
        if( file_name[file_name.size()-1].find(".h5") ){
            
            cv::Ptr<hdf::HDF5> h5io = cv::hdf::open(file_name);

            if(h5io->hlexists(parent_name) && h5io->hlexists(dataset_name))
                h5io->dsread(data, dataset_name);

            h5io->close();
        }
        return data;
    }

    torch::Tensor data_toTensor(std::string&& file_path){ //need to check for dataset dim
        
        cv::Mat data = load_HDF5(std::move(file_path));

        if(!(data[0].rows == data[0].cols == 224))
            cv::resize(img_data, img_data, cv::Size(224,224), cv::INTER_CUBIC);
        
        torch::Tensor tensor_tensor = torch::from_blob(img_data.data, {img_data.rows, img_data.cols, img_data.channels, img_data.size(img_data.dims - 1) }, torch::kBytes);
        img_tensor = img.tensor.permute({3,2,0,1});

        return img_tensor;
    }

    torch::Tensor label_toTensor(std::string&& file_path){ //will throw runtime err if cond not true, needs log

        cv::Mat data = load_HDF5(std::move(file_path));
        
        if(data.dims == 1)
            torch::Tensor labels = torch::full({1}, data);

        return labels;
    }


}
