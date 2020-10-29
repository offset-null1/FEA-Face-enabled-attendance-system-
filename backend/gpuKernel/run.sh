nvcc -c -g -G median_blur.cu 
g++ -o main  main.cpp median_blur.o `pkg-config opencv --cflags --libs` -L/usr/local/cuda/lib64 -lcuda -lcudart 
./main