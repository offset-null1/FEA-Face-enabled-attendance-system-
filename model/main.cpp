#include <iostream>
#include <torch/torch.h>
#include "include/load.hpp"
#include "include/train.hpp"
#include "include/metric.hpp"


int main(int argc, char const *argv[])
{
    if(argc){
        std::cout<<*argv;
    }
   
    return 0;
}

