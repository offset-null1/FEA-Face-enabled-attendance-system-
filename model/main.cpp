#include <iostream>
#include <torch/torch.h>
#include "load.hpp"
#include "train.hpp"
#include "metric.hpp"
#include <string>

int main(int argc, char const *argv[])
{
    if((argc == 1) || (argc > 3)){
        std::cout<<"[USE]: pass first dataset and then target labels filepath(HDF5) as the argument" << '\n';
        return -1;
    }

    std::string data_path{argv[1]}; //load arguments
    std::string labels_path{argv[2]};

    auto dataset_loader = loader::loadDataset( std::move(data_path), std::move(labels_path) ).map(torch::data::transforms::Stack<>()); //utility to load images from hdf5 dataset to torch::Tensor
    std::cout<< &dataset_loader;
    
    
    
    
    return 0;
}

