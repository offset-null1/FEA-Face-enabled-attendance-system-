#include <iostream>
#include <torch/torch.h>
#include <torch/script.h>
#include <chrono>
#include <vector>
#include <string> 
#include "load.hpp"
#include "metric.hpp"

torch::Device get_device(){
    
    if(torch::cuda::is_available()){
        std::cout<< "Using CUDA" <<'\n';
        return torch::kCUDA; //returns 1
    }
    else{
        std::cout<< "Using CPU" <<'\n';
        return torch::kCPU; //returns 0
    }
}

template<typename Dataloader>
void train_net(Dataloader& data_loader, torch::jit::script::Module net, torch::optim::Optimizer& optimizer, torch::nn::Linear lin, const int epoch, size_t dataset_size){

    auto start = std::chrono::system_clock::now();

    std::vector<float> acc_history;
    float best_acc = 0.0f;
    int batch_index();

    torch::Device device_ = get_device();

    for(int i=0 ; i<epoch ; ++i){
        std::cout << "Epoch" << i+1 <<'/'<< epoch << "\n\n";
    
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
        running_loss = running_loss/(float)(batch_index); //avg
        std::cout << "Epoch" << i << ", " << "Accuracy: " << running_corrects/dataset_size << ", " << running_loss << '\n';
    }


    auto end = std::chrono::system_clock::now();

    std::chrono::duration<double> difference = end - start;
    std::cout << "Time consumed for training :" << difference.count() << "\n\n"; 
}

template<typename Dataloader>
void test(Dataloader& loader, torch::jit::script::Module net, torch::nn::Linear lin, size_t dataset_size){

    net.eval();

    float running_loss = 0.0f, running_accuracy = 0.0f;

    for(const auto& batch : *loader){

        auto data = batch.data;
        auto labels = batch.labels.squeeze();

        torch::Device device_ = get_device();
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