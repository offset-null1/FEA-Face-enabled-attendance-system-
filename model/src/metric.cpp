#define _USE_MATH_DEFINES

#include <torch/torch.h>
#include <iostream>
#include <math.h>
#include "../include/loss.h"


namespace metric{

    using namespace torch;
    using namespace std;
    namespace DT = data::transforms;

    arcMarginImpl::arcMarginImpl(int64_t N, int64_t M, float s, float m, bool easy_margin) : N(N),M(M),s(s),m(m),easy_margin(easy_margin),fc(torch::nn::LinearOptions(N,M).with_bias(false))
    {
       register_module("fc",fc);
       Tensor weight = register_parameter( "weight", torch::ones((N, M), torch::TensorOptions(torch::kFloat16).requires_grad(true)) );
       nn::init::xavier_uniform_(weight);

       float cos_m = cos(m);
       float sin_m = sin(m);
       float cos_comp = cos(M_PIl - m); //cos(pi-m) = -cos(m)
       float mm = sin(M_1_PIl - m)*m; //cos'(m)
    }


    torch::Tensor loss::arcMarginImpl::forward(const Tensor& input, const Tensor& label)
    {
       
        auto norm_in = ( input - input.mean() ) / input.std();
        auto norm_w = ( weight - weight.mean() ) / weight.std();
        
        auto cosine =  fc->forward(norm_in.view({norm_in.size(0),this->N})); //cos(b)
        auto sine = torch::sqrt( (1.0 - at::pow(cosine, 2)) );
        auto phi = cosine * cos_m - sine * sin_m; //cos(a+b)

        if(easy_margin){
            phi = at::where(cosine>0, phi, cosine);
        }else{
            phi = at::where(cosine>cos_comp, phi, (cosine - mm));
        }

        Tensor one_hot = torch::zeros( cosine.size(cosine.dim()), torch::TensorOptions(torch::kFloat16) );
        one_hot.scatter_(1, label, 1);
        Tensor output = (one_hot * phi) + ((1.0f - one_hot) * cosine) * s;
        
        return output;
    }

}

