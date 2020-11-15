#include <iostream>
#include <torch/torch.h>
#include <torch/script.h>
#include <chrono>
#include <vector>
#include <string> 
#include "include/load.hpp"
#include "include/loss.h"

#define s 0.00
#define m 0.00

torch::device get_device(){
    
    if(torch::cuda::is_available()){
        std::cout<< "Using CUDA" <<'\n';
        device_ =  torch::kCUDA; //returns 1
    }
    else{
        std::cout<< "Using CPU" <<'\n';
        device_ = torch::kCPU; //returns 0
    }
}

void train_net(loader::loadDataset& data_loader, torch::jit::module net, torch::optim::Optimizer& optimizer ,torch::nn::Linear fc, const int epochs, bool use_default_loss, bool test){

    auto start = std::chrono::system_clock::now();

    std::vector<float> acc_history;
    float best_acc = 0.0f;

    torch::device device_ = get_device();

    for(int i=0 ; i<epochs ; ++i){
        std::cout << "Epoch" << i+1 <<'/'<< epochs << '\n\n';

        if(test){
            net.eval();
        }
        else{
            net.train();
        }

        float running_loss = 0.0f;
        int16_t running_corrects = 0;

        for(auto& batch : *data_loader){
            data = data.to(device_);
            labels = labels.to(device_);

            std::vector<torch::jit::IValue> input;
            input.push_back(data);
            optimizer.zero_grad();

            auto output = net.forward(input).toTensor();
            output = output.view({output.size(0), -1});

            auto loss = torch::nll_loss(torch::binary_cross_entropy_with_logits(output, 1), labels);
            loss.backward();
            optimizer.step();

            

        }
        

    }


    auto end = std::chrono::system_clock::now();

    std::chrono::duration<double> difference = end - start;
    std::cout << "Time consumed for training :" << difference.count() << '\n\n'; 
}