#include<torch/torch.h>
#include<iostream>


struct arcMarginProd : torch::nn::Module{
    arcMarginProd(torch::Tensor& in_features, torch::Tensor& out_features, float s=30.0, float m=0.50, bool easy_margin=false){
        // in_features = register_parameter("in_features",in_features);
        // out_features = register_parameter("out_features",out_features);
        // s = register_parameter("s",s);
        // m = register_parameter("m",m);
        weight = register_parameter("weight",torch::nn::init::xavier_uniform_());
        
    }

}







int main(){
    torch::Tensor tensor = torch::eye(3);
    std::cout<<tensor<<std::endl;
    
}