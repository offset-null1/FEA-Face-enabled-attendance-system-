#include <iostream>
#include <vector>
#include <torch/torch.h>
#include "../include/loss.h"
#include "../include/resnet.h"

    torch::Device device_ = torch::kCPU;

    inline torch::nn::Conv2dOptions setConvOpt(int64_t in_channel, int64_t out_channel, int64_t kernel_size=3, int64_t stride=1, int64_t padding=0, bool with_bias=false){
        return torch::nn::Conv2dOptions(in_channel,out_channel,kernel_size).stride(stride).padding(padding).with_bias(with_bias); 
    }


    baseBlock::baseBlockImpl(int64_t inChannel, int64_t outchannel, int64_t stride=1)
        :   stride(stride),
            conv1(setConvOpt(inChannel,outchannel,stride)),
            bn1(outchannel),
            conv2(setConvOpt(inChannel,outchannel,stride)),
            bn2(outchannel)
        {
            register_module("conv1", conv1);
            register_module("bn1", bn1);
            register_module("conv2", conv2);
            register_module("bn2", bn2);

            bool condition = (inChannel!=outchannel);

            if(condition){
                downsample(setConvOpt(inChannel,outchannel,1,2);
                register_module("downsample", downsample);
            }

            if(torch::cuda::is_available()){
                std::cout << "Using CUDA for training" << '\n';
                device_ = torch::kCUDA;
                
                c1->to(device_);
                c2->to(device_);
                b1->to(device_);
                b2->to(device_);
                if(condition)
                    downsample->to(device_);
            }

        }

   

    torch::Tensor baseBlockImpl::forward(torch::Tensor x){

        at::Tensor identity(x.clone());

        x = conv1->forward(x);
        x = bn1->forward(x);
        x = torch::relu(x);

        x = conv2->forward(x);
        x = bn2->forward(x);

        if(!downsample->is_empty()){
            identity = downsample->forward(identity);
        }
        x+=identity;
        x = torch::relu(x);

        return x;
    }


    resnetImpl::resnetImpl(std::vector<int64_t> layers, int64_t classes)
        :   conv1(setConvOpt(3, 64, 7, 2, 3)),
            bn1(64), //channels
            layer1(make_layer(64, layers[0])),
            layer2(make_layer(128, layers[1], 2)),
            layer3(make_layer(256, layers[2], 2)),
            layer4(make_layer(512, layers[3], 2)),
            fc(512 * num_layers, classes)
        {
            register_module("conv1", conv1);
            register_module("bn1", bn1);
            register_module("layer1", layer1);
            register_module("layer2", layer2);
            register_module("layer3", layer3);
            register_module("layer4", layer4);
            register_module("fc", fc);
        }


    torch::Tensor resnetImpl::forward(torch::Tensor x){
        x = conv1->forward(x);
        x = bn1->forward(x);
        x = torch::relu(x);
        x = torch::max_pool2d(x, 3, 2, 1);

        x = layer1->forward(x);
        x = layer2->forward(x);
        x = layer3->forward(x);
        x = layer4->forward(x);

        x = torch::avg_pool2d(x, 7, 1);
        x = x.view({x.sizes()[0], -1});
        x = fc->forward(x);

        return x;
    }
        
        
