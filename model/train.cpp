#include <iostream>
#include <torch/torch.h>
#include <torch/script.h>
#include <chrono>
#include <vector>
#include <string> 
#include "include/load.hpp"
#include "include/loss.h"

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

void train_net(loader::loadDataset& data_loader, torch::jit::module net, torch::optim::Optimizer& optimizer ,  ,torch::nn::Linear lin, const int epochs, size_t dataset_size){

    auto start = std::chrono::system_clock::now();

    std::vector<float> acc_history;
    float best_acc = 0.0f;
    int batch_index();

    torch::device device_ = get_device();

    for(int i=0 ; i<epochs ; ++i){
        std::cout << "Epoch" << i+1 <<'/'<< epochs << '\n\n';
    
        net.train();
        
        float running_loss = 0.0f;
        int16_t running_corrects = 0;

        for(auto& batch : *data_loader){
            
            auto data = batch.data;
            auto labels = batch.labels.squeeze();
            
            data = data.to(device_);
            labels = labels.to(device_);

            std::vector<torch::jit::IValue> input;
            input.push_back(data);
            optimizer.zero_grad();

            auto output = net.forward(input).toTensor();
            output = output.view({output.size(0), -1});
            output = lin(output); //linear layer

            auto loss = torch::binary_cross_entropy_with_logits(output, labels);
            loss.backward();
            optimizer.step();

            auto acc = output.argmax(1).eq(labels).sum();

            running_corrects = acc.template item<float>(); 
            running_loss = loss.template item<float>();

            batch_index +=1;            

        }
        running_loss = running_loss/float(batch_index); //avg
        std::cout << "Epoch" << i << ", " << "Accuracy: " << running_corrects/dataset_size << ", " << running_loss << '\n';
    }


    auto end = std::chrono::system_clock::now();

    std::chrono::duration<double> difference = end - start;
    std::cout << "Time consumed for training :" << difference.count() << '\n\n'; 
}


void test(loader::loadDataset& loader, torch::jit::script::Module net, torch::nn::Linear lin, size_t dataset_size){

    net.eval();

    float running_loss = 0.0f, running_accuracy = 0.0f;

    for(const auto& batch : *loader){

        auto data = batch.data;
        auto labels = batch.labels.squeeze();

        torch::data device_ = get_device();
        data.to(device_);
        labels.to(device_);

        std::vector<torch::jit::IValue> input;
        input.push_back(data);

        torch::Tensor output = net.forward(input).toTensor();
        output = output.view({output.size(0), -1});
        output = lin(output);

        auto loss = torch::binary_cross_entropy_with_logits(output, labels);

        auto acc = output.argmax(1).eq(labels).sum();
        running_loss = loss.template item<float>(); 
        running_accuracy = acc.template item<float>();

    }
    std::cout << "Test loss:" << running_loss/dataset_size << ", Accuracy:" << running_accuracy/dataset_size << '\n';
}