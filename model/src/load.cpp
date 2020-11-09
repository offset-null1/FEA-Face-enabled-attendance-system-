#include <experimental/filesystem>
#include <iostream>
#include <vector>

namespace fs = std::experimental::filesystem;

Val load(const fs::path& pickle_file) {
    std::cout<<fs::absolute(pickle_file);
    Val results;
    LoadValFromFile(pickle_file, results SERIALIZE_P2);
    return results;

}

int main(){

    
    return 0;
}