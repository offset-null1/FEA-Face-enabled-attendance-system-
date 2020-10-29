#define _USE_MATH_DEFINES

#include <torch/torch.h>
#include <iostream>
#include <math.h>
#include <utility>
#include <variant>


namespace loss{

    using namespace torch;
    using namespace std;

    namespace DT = data::transforms;

    struct arcMarginProd : nn::Module{
        arcMarginProd(int64_t N, int64_t M, float s=30.0, float m=0.50, bool easy_margin=false) 
        : N(N),
          M(M),
          s(s),
          m(m),
          easy_margin(easy_margin)
        {
           fc = register_module("fc", nn::Linear(N,M) );
           Tensor weight = register_parameter( "weight", at::ones((N, M)) );
           nn::init::xavier_uniform_(weight);

           float cos_m = cos(m);
           float sin_m = sin(m);
           float cos_comp = cos(M_PIl - m);
           float mm = sin(M_1_PIl - m)*m;

        }

        torch::Tensor forward(const Tensor& input, const Tensor& label){
       
            Tensor norm_in = input - at::mean(input, input.dim(),true) / at::std(input, input.dim(), true);
            Tensor norm_w = weight - at::mean(weight, weight.dim(), true) / at::std(weight, weight.dim(), true);
            
            Tensor cosine =  fc->forward(norm_in.reshape({norm_in.size(0),this->N}));
            Tensor sine = torch::sqrt( (1.0 - at::pow(cosine, 2)) );
            Tensor phi = cosine * cos_m - sine * sin_m;

            if(easy_margin){
                phi = at::where(cosine>0, phi, cosine);
            }else{
                phi = at::where(cosine>cos_comp, phi, (cosine - mm));
            }

            Tensor one_hot = at::zeros( cosine.size(cosine.dim()) );
            one_hot.scatter_(1, label, 1);
            Tensor output = (one_hot * phi) + ((1.0f - one_hot) * cosine) * s;
            return output;
        }

            int64_t N;
            int64_t M; 
            float s; 
            float m;
            bool easy_margin;
            torch::Tensor weight;
            torch::nn::Linear fc{nullptr};

            float cos_m;
            float cos_comp;
            float sin_m;
            float mm;

    };

}
