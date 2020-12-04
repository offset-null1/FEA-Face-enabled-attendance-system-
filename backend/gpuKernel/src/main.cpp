#include<iostream>
#include<opencv2/opencv.hpp>
#include<opencv2/highgui.hpp>
#include "median_f.h"

using namespace std;
using namespace cv;

int main(){
   
    Mat in_frame = imread("/path/to/image", IMREAD_GRAYSCALE);
    if(in_frame.empty()){
        cout<<"Empty"<<"\n";
        return 1;
    }
    resize(in_frame,in_frame,Size(600,600));
    // imshow("window",img);
    // if((int)waitKey(0)=='s'){
    //    destroyAllWindows(); 
    // }
   
    Mat out_frame(Size(in_frame.rows,in_frame.cols), CV_8UC1);

    unsigned char* data = in_frame.data;
    take_input(in_frame,out_frame);

    Mat res;
    medianBlur(in_frame,res,3);
    imshow("in",in_frame);
    imshow("out",out_frame);
    imshow("res",res);

    waitKey(0);

return 0;
}
