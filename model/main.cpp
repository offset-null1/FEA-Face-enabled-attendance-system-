#include <iostream>
#include <torch/torch.h>
#include "load.hpp"
#include "train.hpp"
#include "metric.hpp"
#include <string>

int main(int argc, char const *argv[])
{
    if((argc == 1) || (argc > 4)){
        std::cout<<"[USE]: pass first jit Model ,dataset and then target labels filepath(HDF5) as the argument" << '\n';
        return -1;
    }

    torch::jit::script::Module net = torch::jit::load(argv[1]);
    std::string data_path{argv[2]}; //load arguments
    std::string labels_path{argv[3]};


    auto dataset_loader = loader::loadDataset( std::move(data_path), std::move(labels_path) ).map(torch::data::transforms::Stack<>()); //utility to load images from hdf5 dataset to torch::Tensor
    
    // Resource: https://discuss.pytorch.org/t/how-to-load-the-prebuilt-resnet-models-or-any-other-prebuilt-models/40269/8
    torch::nn::Linear lin(512, 2);  // the last layer of resnet, which you want to replace, has dimensions 512x1000
    torch::optim::Adam opt(lin->parameters(), torch::optim::AdamOptions(1e-3 /*learning rate*/));

    auto data_loader = torch::data::make_data_loader<torch::data::samplers::RandomSampler>(std::move(dataset_loader), 4);
    // train_net(data_loader, net, opt, lin, dataset_loader.size());
    std::cout<<dataset_loader.size();
    return 0;
}

